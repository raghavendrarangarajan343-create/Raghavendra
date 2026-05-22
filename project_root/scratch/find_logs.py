import os

def read_config():
    config_path = r"C:\ProgramData\Jenkins\.jenkins\jobs\validation_pipeline\config.xml"
    if os.path.exists(config_path):
        print(f"=== config.xml found at {config_path} ===")
        with open(config_path, "r", encoding="utf-8", errors="ignore") as f:
            print(f.read())
    else:
        print(f"config.xml not found at {config_path}")

if __name__ == "__main__":
    read_config()
