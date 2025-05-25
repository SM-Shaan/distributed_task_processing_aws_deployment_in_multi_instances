## Troubleshooting Common Issues

### 1. Chocolatey Not Recognized

If you see this error:
```
choco : The term 'choco' is not recognized...
```
It means Chocolatey (the Windows package manager) is not installed or not in your system's PATH.

#### How to Install Chocolatey

1. **Open PowerShell as Administrator:**
    - Click Start (or press `Win + S`)
    - Type `powershell`
    - Right-click **Windows PowerShell** and select **Run as Administrator**

2. **Install Chocolatey:**
    Paste the following into the PowerShell window:
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; `
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

3. **Verify Installation:**
    - Close PowerShell, open a new terminal, and run:
      ```powershell
      choco --version
      ```
    - You should see a version number (e.g., `1.4.0`).

4. **(If Needed) Add Chocolatey to PATH for Current Session:**
    ```powershell
    $env:Path += ";C:\ProgramData\chocolatey\bin"
    ```
    Then install Pulumi:
    ```powershell
    choco install pulumi -y
    ```

---

### 2. Setting Up SSH Key Pair

To generate and use an SSH key pair for AWS EC2:

1. **Generate Key Pair:**
    ```sh
    ssh-keygen -t rsa -b 2048 -f app-key-pair
    ```
    Press Enter twice when prompted for a passphrase.

2. **Extract Public Key:**
    ```sh
    cat app-key-pair.pub
    ```
    Copy the entire output (starts with `ssh-rsa`).

3. **Update Pulumi Script:**
    - In your Pulumi `main.py`, find the `aws.ec2.KeyPair` resource and replace the public key with your copied value.

---

### 3. Pulumi Access Token Error

If you see:
```
error: invalid access token
```
Pulumi needs you to log in.

#### How to Fix

- **Option 1 (Recommended):**  
  When prompted, just press `<ENTER>` to use browser-based login. Complete authentication in your browser.

- **Option 2:**  
  Enter a valid access token from https://app.pulumi.com/account/tokens when prompted.

---

For more details, refer to the project documentation or the official Pulumi and Chocolatey guides.
