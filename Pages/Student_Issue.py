import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Student Issues Merger & Filter", layout="wide")
st.title("📚 Student Issues - Merge & Filter")

# Sidebar for file uploads
st.sidebar.header("📁 Upload Files")
st.sidebar.markdown("Upload two files to merge them together")

# File uploader for TWO files
uploaded_files = st.sidebar.file_uploader(
    "Choose Excel or CSV files (upload 2 files)",
    type=['xlsx', 'xls', 'csv'],
    accept_multiple_files=True,
    help="Upload 2 files with the same structure to merge them"
)

# Load data function with caching
@st.cache_data
def load_data(file):
    """Load data from uploaded file"""
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df

# Check if files are uploaded
if uploaded_files is not None and len(uploaded_files) > 0:
    
    # Load all uploaded files
    dataframes = []
    file_names = []
    
    for file in uploaded_files:
        try:
            df = load_data(file)
            dataframes.append(df)
            file_names.append(file.name)
            st.sidebar.success(f"✅ Loaded: {file.name} ({len(df)} rows)")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading {file.name}: {str(e)}")
    
    # Merge the dataframes if multiple files uploaded
    if len(dataframes) > 0:
        st.sidebar.markdown("---")
        st.sidebar.info(f"📊 Total files uploaded: {len(dataframes)}")
        
        # Merge/concatenate all dataframes
        if len(dataframes) == 1:
            merged_df = dataframes[0]
            st.info("ℹ️ Only one file uploaded. Showing data from that file.")
        else:
            # Concatenate all dataframes (stack them vertically)
            merged_df = pd.concat(dataframes, ignore_index=True)
            st.success(f"✅ Successfully merged {len(dataframes)} files! Total rows: {len(merged_df)}")
            
            # Show merge details
            with st.expander("📋 Merge Details"):
                for i, (name, df) in enumerate(zip(file_names, dataframes), 1):
                    st.write(f"**File {i}:** {name} - {len(df)} rows")
        
        # Now work with the merged dataframe
        df = merged_df
        
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Filter Options")
        
        # Filter 1: Class
        if 'Class' in df.columns:
            classes = ['All'] + sorted(df['Class'].dropna().unique().tolist())
            selected_class = st.sidebar.selectbox('Select Class:', classes)
            
            # Apply first filter
            if selected_class != 'All':
                df_temp = df[df['Class'] == selected_class]
            else:
                df_temp = df.copy()
        else:
            st.warning("⚠️ 'Class' column not found!")
            df_temp = df.copy()
        
        # Filter 2: Subject (dynamic based on Class)
        if 'Subject' in df.columns:
            subjects = ['All'] + sorted(df_temp['Subject'].dropna().unique().tolist())
            selected_subject = st.sidebar.selectbox('Select Subject:', subjects)
            
            # Apply second filter
            if selected_subject != 'All':
                df_temp = df_temp[df_temp['Subject'] == selected_subject]
        else:
            st.warning("⚠️ 'Subject' column not found!")
            selected_subject = 'All'
        
        # Filter 3: Teacher (dynamic based on Class and Subject)
        if 'Resolver Teacher' in df.columns:
            teachers = ['All'] + sorted(df_temp['Resolver Teacher'].dropna().unique().tolist())
            selected_teacher = st.sidebar.selectbox('Select Teacher:', teachers)
            
            # Apply third filter
            if selected_teacher != 'All':
                filtered_df = df_temp[df_temp['Resolver Teacher'] == selected_teacher]
            else:
                filtered_df = df_temp
        else:
            st.warning("⚠️ 'Resolver Teacher' column not found!")
            filtered_df = df_temp
        
        # Display filter summary in sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("📈 Summary")
        st.sidebar.metric("Total Merged Records", len(df))
        st.sidebar.metric("Filtered Records", len(filtered_df))
        st.sidebar.metric("Hidden Records", len(df) - len(filtered_df))
        
        # Main content area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"📊 Filtered Results: {len(filtered_df)} records")
        
        with col2:
            # Search functionality
            search_term = st.text_input("🔎 Search:", "", placeholder="Search...")
        
        # Apply search filter
        if search_term:
            mask = filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
            filtered_df = filtered_df[mask]
            st.info(f"🔍 Found {len(filtered_df)} records matching '{search_term}'")
        
        # Display results
        if len(filtered_df) > 0:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                height=500
            )
            
            # Download section
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                # Download as CSV
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="merged_filtered_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Download as Excel
                from io import BytesIO
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Merged Data')
                
                st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name="merged_filtered_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col3:
                # Option to download original merged data (before filters)
                if len(df) != len(filtered_df):
                    csv_all = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download All Merged Data",
                        data=csv_all,
                        file_name="all_merged_data.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # Display statistics
            st.markdown("---")
            st.subheader("📊 Quick Statistics")
            
            stat_cols = st.columns(4)
            
            with stat_cols[0]:
                if 'Class' in filtered_df.columns:
                    st.metric("Unique Classes", filtered_df['Class'].nunique())
            
            with stat_cols[1]:
                if 'Subject' in filtered_df.columns:
                    st.metric("Unique Subjects", filtered_df['Subject'].nunique())
            
            with stat_cols[2]:
                if 'Resolver Teacher' in filtered_df.columns:
                    st.metric("Unique Teachers", filtered_df['Resolver Teacher'].nunique())
            
            with stat_cols[3]:
                st.metric("Files Merged", len(dataframes))
        
        else:
            st.warning("⚠️ No matching records found.")
            st.info("""
            **💡 Tips:**
            - Try different filter combinations
            - Clear search term if used
            - Select 'All' in filters to see more data
            """)

else:
    # No files uploaded - show instructions
    st.info("👈 **Please upload files to get started**")
    
    st.markdown("""
    ### 📋 How to Use:
    
    1. **Upload 2 files** using the file uploader in the sidebar
       - Both files should have the same column structure
       - Supported formats: Excel (.xlsx, .xls) or CSV (.csv)
    
    2. **Files will be automatically merged** (stacked together)
       - All rows from both files will be combined
       - Duplicate rows are kept (not removed)
    
    3. **Filter the merged data**:
       - Class (e.g., 9th, 10th, 11th)
       - Subject (e.g., SST, Math, Science)
    
    4. **Download your results**:
       - Filtered data only
       - All merged data (before filters)
    
    ### 📊 Required Columns:
    Your files should contain:
    - `Class` - Student class/grade
    - `Subject` - Subject name

    
    ### 💡 Tip:
    You can upload more than 2 files - all will be merged together!
    """)
    