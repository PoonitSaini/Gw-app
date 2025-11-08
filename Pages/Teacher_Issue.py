import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Student Issues Merger & Filter", layout="wide")
st.title("📚 Student Issues - Merge & Filter (Multi-Select)")

# Sidebar for file uploads
st.sidebar.header("📁 Upload Files")
st.sidebar.markdown("Upload two or more files to merge them together")

# File uploader for multiple files
uploaded_files = st.sidebar.file_uploader(
    "Choose Excel or CSV files",
    type=['xlsx', 'xls', 'csv'],
    accept_multiple_files=True,
    help="Upload 2+ files with the same structure to merge them"
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
        st.sidebar.header("🔍 Filter Options (Multi-Select)")
        st.sidebar.markdown("Select multiple options from each filter:")
        
        # Multi-select Filter 1: Issue In Class
        if 'Issue In Class' in df.columns:
            selected_classes = st.sidebar.multiselect(
                'Select Classes:',
                options=sorted(df['Issue In Class'].dropna().unique().tolist()),
                default=[],
                help="Select one or more classes. Leave empty to show all classes."
            )
            
            # Apply first filter
            if selected_classes:
                df_temp = df[df['Issue In Class'].isin(selected_classes)]
            else:
                df_temp = df.copy()
        else:
            st.warning("⚠️ 'Issue In Class' column not found!")
            df_temp = df.copy()
        
        # Multi-select Filter 2: Issue In Subject (dynamic based on Class selection)
        if 'Issue In Subject' in df.columns:
            available_subjects = sorted(df_temp['Issue In Subject'].dropna().unique().tolist())
            selected_subjects = st.sidebar.multiselect(
                'Select Subjects:',
                options=available_subjects,
                default=[],
                help="Select one or more subjects. Options update based on class selection."
            )
            
            # Apply second filter
            if selected_subjects:
                df_temp = df_temp[df_temp['Issue In Subject'].isin(selected_subjects)]
        else:
            st.warning("⚠️ 'Issue In Subject' column not found!")
            selected_subjects = []
        
        # Multi-select Filter 3: Teachers Name (dynamic based on Class and Subject)
        if 'Teachers Name' in df.columns:
            available_teachers = sorted(df_temp['Teachers Name'].dropna().unique().tolist())
            selected_teachers = st.sidebar.multiselect(
                'Select Teachers:',
                options=available_teachers,
                default=[],
                help="Select one or more teachers. Options update based on previous selections."
            )
            
            # Apply third filter
            if selected_teachers:
                filtered_df = df_temp[df_temp['Teachers Name'].isin(selected_teachers)]
            else:
                filtered_df = df_temp
        else:
            st.warning("⚠️ 'Teachers Name' column not found!")
            filtered_df = df_temp
        
        # Additional Filter: Issue Type
        if 'Issue Type' in df.columns:
            available_issue_types = sorted(df_temp['Issue Type'].dropna().unique().tolist())
            selected_issue_types = st.sidebar.multiselect(
                'Select Issue Types:',
                options=available_issue_types,
                default=[],
                help="Select one or more issue types."
            )
            
            if selected_issue_types:
                filtered_df = filtered_df[filtered_df['Issue Type'].isin(selected_issue_types)]
        
        # Additional Filter: Final Status
        if 'Final Status' in df.columns:
            available_status = sorted(df_temp['Final Status'].dropna().unique().tolist())
            selected_status = st.sidebar.multiselect(
                'Select Final Status:',
                options=available_status,
                default=[],
                help="Select one or more status."
            )
            
            if selected_status:
                filtered_df = filtered_df[filtered_df['Final Status'].isin(selected_status)]
        
        # Add a reset button in sidebar
        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
            st.rerun()
        
        # Display filter summary in sidebar
        st.sidebar.markdown("---")
        st.sidebar.subheader("📈 Summary")
        st.sidebar.metric("Total Merged Records", len(df))
        st.sidebar.metric("Filtered Records", len(filtered_df))
        st.sidebar.metric("Hidden Records", len(df) - len(filtered_df))
        st.sidebar.metric("Files Merged", len(dataframes))
        
        # Display active filters
        active_filters = []
        if selected_classes:
            active_filters.append(f"**Classes:** {', '.join(map(str, selected_classes))}")
        if selected_subjects:
            active_filters.append(f"**Subjects:** {', '.join(map(str, selected_subjects))}")
        if selected_teachers:
            active_filters.append(f"**Teachers:** {', '.join(map(str, selected_teachers))}")
        
        if active_filters:
            st.sidebar.markdown("---")
            st.sidebar.subheader("🎯 Active Filters")
            for filter_text in active_filters:
                st.sidebar.write(filter_text)
        
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
                    label="📥 Download Filtered CSV",
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
                    label="📥 Download Filtered Excel",
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
            
            stat_cols = st.columns(5)
            
            with stat_cols[0]:
                if 'Issue In Class' in filtered_df.columns:
                    st.metric("Unique Classes", filtered_df['Issue In Class'].nunique())
            
            with stat_cols[1]:
                if 'Issue In Subject' in filtered_df.columns:
                    st.metric("Unique Subjects", filtered_df['Issue In Subject'].nunique())
            
            with stat_cols[2]:
                if 'Teachers Name' in filtered_df.columns:
                    st.metric("Unique Teachers", filtered_df['Teachers Name'].nunique())
            
            with stat_cols[3]:
                if 'Issue Type' in filtered_df.columns:
                    st.metric("Issue Types", filtered_df['Issue Type'].nunique())
            
            with stat_cols[4]:
                st.metric("Total Rows", len(filtered_df))
            
            # Optional: Show distribution charts
            if st.checkbox("📈 Show Data Distribution"):
                chart_col1, chart_col2, chart_col3 = st.columns(3)
                
                with chart_col1:
                    if 'Issue In Class' in filtered_df.columns and len(filtered_df['Issue In Class'].value_counts()) > 0:
                        st.write("**Distribution by Class:**")
                        st.bar_chart(filtered_df['Issue In Class'].value_counts())
                
                with chart_col2:
                    if 'Issue In Subject' in filtered_df.columns and len(filtered_df['Issue In Subject'].value_counts()) > 0:
                        st.write("**Distribution by Subject:**")
                        st.bar_chart(filtered_df['Issue In Subject'].value_counts())
                
                with chart_col3:
                    if 'Issue Type' in filtered_df.columns and len(filtered_df['Issue Type'].value_counts()) > 0:
                        st.write("**Distribution by Issue Type:**")
                        st.bar_chart(filtered_df['Issue Type'].value_counts())
        
        else:
            st.warning("⚠️ No matching records found.")
            st.info("""
            **💡 Tips:**
            - Try selecting different filters
            - Clear search term if used
            - Leave filters empty to see all merged data
            - Click 'Reset All Filters' button
            """)
            
            # Show what filters are active
            if active_filters:
                st.markdown("### Currently Active Filters:")
                for filter_text in active_filters:
                    st.write(filter_text)

else:
    # No files uploaded - show instructions
    st.info("👈 **Please upload files to get started**")
    
    st.markdown("""
    ### 📋 How to Use:
    
    1. **Upload 2+ files** using the file uploader in the sidebar
       - Both files should have the same column structure
       - Supported formats: Excel (.xlsx, .xls) or CSV (.csv)
    
    2. **Files will be automatically merged** (stacked together)
       - All rows from both files will be combined
       - Duplicate rows are kept (not removed)
    
    3. **Download your results**:
       - Filtered data only
       - All merged data (before filters)
    
   
    """)
    
   

# Footer
st.markdown("---")

