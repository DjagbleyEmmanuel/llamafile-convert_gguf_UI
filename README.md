# llamafile-convert_gguf_UI
This GUI aims to simplify the process of converting GGUF files to llamafile format by providing an intuitive and convenient way for users to interact with the underlying conversion script.
This program is a simple graphical user interface (GUI) application created using PyQt5 for the purpose of converting files from the GGUF format to llamafile format. The GGUF file can be provided either by entering its path or URL manually or by using the "Browse" button to select a file through a file dialog.

Key features of the program include:

1. **File Selection:** Users can input the file path or URL manually or click the "Browse" button to navigate their file system and select the GGUF file they want to convert.

2. **Conversion Mode:** Users can choose the conversion mode from the provided options: "cli" (command-line interface), "server," or "both." This determines the manner in which the conversion script processes the GGUF file.

3. **Conversion Process:** Upon clicking the "Convert" button, the program executes a shell script designed for the conversion task. The output of the conversion process, including any error messages, is displayed in a text area within the GUI.

4. **Error Handling:** The program incorporates error handling mechanisms, and any unexpected errors during the conversion process are presented to the user through a pop-up message box.

5. **User-Friendly Interface:** The application is designed with a clean and straightforward interface, making it accessible for users with minimal technical expertise.
