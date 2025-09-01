
# 📖 Kartick's Bookmark Manager

A simple desktop tool to **add, edit, and manage PDF bookmarks** with an easy-to-use interface.  
Built with Python and PySide6, packaged as a standalone EXE for Windows.

---

## ✨ Features
- 📂 **Open any PDF** and view its contents with a built-in PDF preview.  
- 🏷️ **Add Chapters & Sections** with custom page numbers.  
- ✏️ **Edit or Remove Bookmarks** easily with the "Edit Selected" and "Remove Selected" buttons.  
- 📑 **Two-column view**: left shows the bookmark structure, right shows corresponding page numbers.  
- 📜 **Page Indicator** (`current_page / total_pages`).  
- 💾 **Export PDF with Bookmarks**: saves as `<original>_With_Bookmark.pdf`.  
- 📂 **Open exported file directly** with a clickable "Open" button.  
- 🖼️ Clean and modern UI with larger fonts for readability.  

---

## 📖 User Manual

### 1. Open a PDF
- Click **Open PDF**.
- Select your PDF file.
- The file will load in the viewer.

### 2. Add a Chapter or Section
- Click **Add Chapter** or **Add Section**.
- Enter a **title** and **page number**.
- The entry will appear in the bookmarks list (with page number on the right).

### 3. Edit or Remove Bookmarks
- Select a bookmark in the list.
- Use **Edit Selected** to change its title or page.
- Use **Remove Selected** to delete it.

### 4. Navigate the PDF
- The **page counter** shows `current_page / total_pages`.

### 5. Export Bookmarked PDF
- Click **Export**.
- A save dialog will appear with `<original>_With_Bookmark.pdf` pre-filled.
- Save it anywhere you like.
- After saving, click **Open** to directly launch the new file.

---

## 💻 Installation

1. Download the latest release from here:  
   👉 [Download Kartick's Bookmark Manager (Windows EXE)]([https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest](https://drive.google.com/file/d/1df9ed4Vp-i8l-T_WYza70673Z7DlkOdZ/view?usp=sharing))

2. Run the EXE file.

3. No installation required — just double-click and start using! ✅

---

## 🛠️ Developer Notes

- **Built with:** Python 3.12  
- **Libraries used:** PySide6, PyMuPDF (fitz)  
- **Packaged using:** PyInstaller

