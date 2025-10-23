# ATGEvals SharePoint Upload Instructions
## Evaluation Reports Deployment Guide

### 📍 Target SharePoint Site
**Site URL:** https://microsoft.sharepoint-df.com/teams/ATGEvals/
**Landing Page:** https://microsoft.sharepoint-df.com/teams/ATGEvals/SitePages/CollabHome.aspx

---

## 🚀 Quick Upload Steps

### Option A: Upload Organized Folders (Recommended)
1. **Navigate to SharePoint Site**
   - Go to: https://microsoft.sharepoint-df.com/teams/ATGEvals/
   - Click on "Documents" in the left navigation

2. **Create Document Library Structure**
   ```
   Documents/
   └── EvaluationReports/
       ├── Reports/           (16 detailed evaluation reports)
       ├── Bug_Analysis/      (16 bug analysis reports)  
       ├── Summaries/         (2 comprehensive summaries)
       ├── Assets/            (CSS, JS, build files)
       └── SharePoint_Landing.html (Main dashboard)
   ```

3. **Upload Process**
   - Create "EvaluationReports" folder in Documents
   - Create subfolders: Reports, Bug_Analysis, Summaries, Assets
   - Drag and drop files from local `SharePoint_Upload` folders to corresponding SharePoint folders

### Option B: Upload ZIP Package
1. Upload the `EvaluationReports_SharePoint.zip` file to SharePoint
2. Extract it in SharePoint using "Extract" option
3. Organize folders as needed

---

## 📊 What You're Uploading

### File Summary:
- **Total Files:** 39
- **Main Reports:** 16 detailed evaluation reports
- **Bug Analysis:** 16 bug analysis documents  
- **Summary Reports:** 2 comprehensive overviews
- **Assets:** 3 supporting files (CSS, JS, build script)
- **Landing Page:** 1 SharePoint-optimized dashboard

### File Organization:
```
📁 Reports/
   📄 evaluation_report_ado_20251021.6_20251021_173708_report.html
   📄 evaluation_report_ado_20251021.6_20251021_175136_report.html
   📄 ... (14 more report files)

📁 Bug_Analysis/  
   📄 evaluation_report_ado_20251021.6_20251021_173708_bugs_analysis.html
   📄 evaluation_report_ado_20251021.6_20251021_175136_bugs_analysis.html
   📄 ... (14 more bug analysis files)

📁 Summaries/
   📄 all_runs_summary.html
   📄 comprehensive_summary.html

📁 Assets/
   📄 style.css (Website styling)
   📄 script.js (Interactive functionality)  
   📄 build.js (Build automation)

📄 SharePoint_Landing.html (Main dashboard - SharePoint optimized)
📄 index.html (Original landing page)
📄 README.md (Documentation)
```

---

## 🎯 After Upload Steps

### 1. Set Up Main Landing Page
- Navigate to the uploaded `SharePoint_Landing.html` 
- Copy its URL for easy access
- Consider pinning it to the site homepage

### 2. Configure Permissions
- Set appropriate access permissions for team members
- Consider read-only access for stakeholders
- Full control for report generators/admins

### 3. Enable Features (Optional)
- **Version History:** Track changes over time
- **Metadata Columns:** Add Date, Report Type, Status columns
- **Alerts:** Notify team when new reports are uploaded
- **Search:** Make reports searchable by content

### 4. Integration Options
- **Pin to Teams:** Add document library to Microsoft Teams channel
- **Quick Access:** Bookmark frequently accessed reports
- **Mobile Access:** Verify reports display well on mobile devices

---

## 🔧 Troubleshooting

### If Files Don't Open Properly:
1. Check if HTML files are blocked by security settings
2. Try opening with "Open in Browser" option
3. Ensure CSS/JS files are in correct Assets folder

### If Permissions Issues:
1. Contact site administrator for proper access
2. Verify you have "Contribute" permissions minimum
3. Check if site has custom permission policies

---

## 📞 Support Information

**Generated on:** October 22, 2025
**Source Repository:** https://github.com/detala_microsoft/EvalSummary
**Files Location:** SharePoint_Upload/ folder  
**ZIP Package:** EvaluationReports_SharePoint.zip

For technical issues with SharePoint upload, contact your IT administrator or SharePoint site owner.