import os
import base64
import eel
import converter                                               #this is the file above (name it converter.py)

eel.init("web")
OUTPUT_DIR = os.path.join(os.getcwd(), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)





@eel.expose
def open_output_folder():
    out = converter.OUTPUT_DIR
    print(f"[main] Open output folder: {out}")
    if os.name == "nt":
        os.startfile(out)  # Windows


@eel.expose
def upload_and_convert(file_name, file_data_base64, output_format):
    """Receive bytes from UI, save to output/, run converter, return saved path."""
    try:
      
        input_path = os.path.join(converter.OUTPUT_DIR, file_name)    # Save uploaded file first
        with open(input_path, "wb") as f:
            f.write(base64.b64decode(file_data_base64))
        print(f"[main] Saved upload -> {input_path}")


        out_path = converter.convert(input_path, output_format)           # Convert
        print(f"[main] Converted -> {out_path}")
        return {"status": "success", "path": out_path}
    except Exception as e:
        print(f"[main] ERROR: {e}")
        return {"status": "error", "message": str(e)}

eel.start("index.html", size=(900, 700))

