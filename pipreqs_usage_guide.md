
# **pipreqs Tool Usage Guide**

## **What is pipreqs?**
`pipreqs` is a Python tool that automatically generates a `requirements.txt` file based on the actual imports used in your Python project. This ensures that your dependency file only contains the libraries you need.

---

## **Installation**
Install pipreqs using pip:
```bash
pip install pipreqs
```

---

## **How to Generate `requirements.txt`**
### Steps:
1. **Navigate to Your Project Directory**:
   Ensure you are in the directory where your Python scripts are located:
   ```bash
   cd /path/to/your/project
   ```

2. **Run pipreqs**:
   Generate a `requirements.txt` file in the current directory:
   ```bash
   pipreqs . --force
   ```
   - `.` indicates the current directory.
   - `--force` overwrites any existing `requirements.txt` file.

---

## **Example Output**
After running pipreqs, the generated `requirements.txt` might look like this:
```plaintext
numpy==1.19.5
tensorflow==2.5.0
matplotlib==3.4.3
```

---

## **Using the Generated `requirements.txt`**
To install the dependencies from the generated `requirements.txt` in a new environment:
```bash
pip install -r requirements.txt
```

---

## **Additional Notes**
- If your project dynamically imports libraries, you may need to manually add those dependencies to the `requirements.txt`.
- You can verify the generated file using:
  ```bash
  cat requirements.txt
  ```

---

## **Resources**
- [pipreqs GitHub Repository](https://github.com/bndr/pipreqs)
