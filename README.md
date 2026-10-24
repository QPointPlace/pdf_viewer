# PDF Viewer

A simple PDF viewer built with **Python**, **PyQt5**, and **PyMuPDF**.

This application provides a lightweight desktop PDF viewer with commonly used features such as opening PDF files, keyword searching, page navigation, drag-and-drop support, and hierarchical table of contents (TOC) navigation.

> This project was created as a learning example for building a desktop PDF viewer using Python and PyQt5.

---

## Features

- Open PDF files
- Drag & Drop support
- Hierarchical Table of Contents (TOC)
- Jump to a selected TOC entry
- Keyword search (`Ctrl + F`)
- Jump to a specified page
- Toolbar and menu
- Save PDF
- Print PDF

---

## Environment

- Python 3.9 or later
- Windows 10 / Windows 11
- PyQt5
- PyMuPDF

The application may also work on Linux and macOS, although it has primarily been tested on Windows.

---

## Installation

Clone this repository.

```bash
git clone https://github.com/QPointPlace/pdf_viewer.git
cd pdf_viewer
```

Create a virtual environment (recommended).

```bash
python -m venv venv
```

Activate it.

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install the required packages.

```bash
pip install PyQt5 PyMuPDF
```

---

## Usage

Run the application.

```bash
python pdf_viewer.py
```

You can:

- Open a PDF from the **File → Open** menu.
- Open a PDF by dragging and dropping it onto the window.
- Press **Ctrl + F** to search.
- Enter a page number and click **Jump**.
- Click an item in the table of contents to move to that page.

---

## Expected Result

After launching the application:

- A PDF file is displayed.
- The table of contents appears in a tree view (if the PDF contains bookmarks).
- Clicking a TOC item jumps to the corresponding page.
- Searching for text moves to the first matching page.
- Drag & Drop opens PDF files.
- Page navigation is available using the page input box.

---

## Project Structure

```text
pdf_viewer/
│
├── pdf_viewer.py
├── README.md
└── LICENSE
```

---

## Dependencies

- PyQt5
- PyMuPDF

Install them with:

```bash
pip install PyQt5 PyMuPDF
```

---

## Future Improvements

Possible future enhancements include:

- Zoom In / Zoom Out
- Continuous scrolling
- Thumbnail view
- Search result highlighting
- Multiple search result navigation
- Recent file history
- Dark mode
- Annotation support

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

You are free to use, modify, and redistribute this software under the terms of the AGPL-3.0 License.

If you distribute modified versions of this software, or make it available over a network as a service, you must also make the complete corresponding source code available under the same license.

For the full license text, see the [LICENSE](LICENSE) file included in this repository.

### Third-Party Libraries

This project depends on the following open-source libraries:

| Library | License |
|---------|---------|
| PyQt5 | GPL v3 or Commercial License |
| PyMuPDF | GNU Affero General Public License v3.0 (AGPL-3.0) |

Please refer to each project's official documentation for detailed licensing information.

---

## Contributing

Contributions are welcome.

If you find this project useful, I'd appreciate it if you:

- ⭐ Star this repository
- 🍴 Fork it if you customize it
- 🐛 Report bugs via Issues
- 💡 Share ideas via Discussions

Pull requests are also welcome.

---

## Acknowledgements

This project is built using the following excellent open-source projects:

- **PyQt5** — Cross-platform GUI framework for Python.
- **PyMuPDF** — High-performance PDF rendering and text extraction library.

Many thanks to the maintainers and contributors of these projects.

- PyQt5
- PyMuPDF
