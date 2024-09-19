import requests
import os
import subprocess
import tarfile

# URL to the JDK archive (choose the correct version and platform)
jdk_url = "https://download.oracle.com/java/17/latest/jdk-17_linux-x64_bin.tar.gz"
# Output path where the JDK will be saved
output_path = "jdk-17_linux-x64_bin.tar.gz"
# Destination directory for the extracted JDK
jdk_dir = "/opt/jdk-17"

# Download the JDK
def download_jdk(url, output_file):
    print(f"Downloading JDK from {url}...")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"JDK downloaded successfully to {output_file}")
    else:
        print(f"Failed to download JDK: Status code {response.status_code}")

# Extract the JDK
def extract_jdk(file_path, destination):
    print(f"Extracting {file_path} to {destination}...")
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(path=destination)
    print("JDK extracted successfully.")

# Configure JAVA_HOME and update PATH
def configure_java_environment(jdk_dir):
    java_home = os.path.abspath(jdk_dir)
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = java_home + "/bin:" + os.environ["PATH"]
    
    print(f"JAVA_HOME set to: {java_home}")
    print(f"PATH updated to include: {java_home}/bin")
    
    # Update /etc/environment for system-wide settings
    with open('/etc/environment', 'a') as f:
        f.write(f"\nJAVA_HOME={java_home}\n")
        f.write(f"PATH={java_home}/bin:$PATH\n")

# Example workflow to download, extract, and set environment variables for JDK
def setup_jdk():
    # Create directory for JDK installation
    if not os.path.exists(jdk_dir):
        os.makedirs(jdk_dir)
        
    download_jdk(jdk_url, output_path)
    extract_jdk(output_path, jdk_dir)
    configure_java_environment(jdk_dir)

if __name__ == "__main__":
    setup_jdk()
