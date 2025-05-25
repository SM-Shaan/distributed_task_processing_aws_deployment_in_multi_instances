Possible issue:

1. The error you're seeing:
```
choco : The term 'choco' is not recognized...
```
means Chocolatey (a Windows package manager) is not installed or not added to your system's PATH.

---

## ✅ Here's exactly what to do (step-by-step)

### 🔵 Step 1: Open **PowerShell** — Not CMD

1. **Click Start** (or press `Win + S`)
2. Type: `powershell`
3. **Right-click** on **Windows PowerShell**
4. Click **Run as Administrator**

> ✅ You must see something like:
>
> ```
> Windows PowerShell
> Copyright (C) ...
> PS C:\Windows\System32>
> ```

---

### 🟢 Step 2: Paste this into PowerShell

Copy and paste the **entire block below** into the **PowerShell terminal** (you should see `PS` at the start of the line):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

✅ This will download and install **Chocolatey**.

---

### 🟡 Step 3: Verify Installation

After installation completes:

1. Close the PowerShell window
2. Open a **new terminal** (PowerShell or CMD)
3. Type:

```powershell
choco --version
```

You should see something like:

```powershell
1.4.0
```

---
Please run this in PowerShell:

$env:Path += ";C:\ProgramData\chocolatey\bin"
Then immediately run:

choco install pulumi -y
If that works, you’ve fixed the problem for the current session.


2. how to Replace with your public key:

Generate an SSH Key Pair:
```
ssh-keygen -t rsa -b 2048 -f app-key-pair
```
When prompted for a passphrase, just press Enter twice (once for passphrase, once for confirmation).

Extract the Public Key:
Open the app-key-pair.pub file to get the public key:

cat app-key-pair.pub
Example output:

ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... user@machine
Copy the entire public key string (starting with ssh-rsa and ending before any trailing whitespace or comments like user@machine).

Update the Pulumi Script:
In the Pulumi script (main.py), locate the aws.ec2.KeyPair resource.

3. You're seeing this error because Pulumi is expecting you to log in to the Pulumi Cloud, but the access token you entered is either missing or incorrect:

error: invalid access token
✅ You Have Two Options to Fix This:
Option 1: Use the Browser-Based Login (Recommended)
When prompted:

Enter your access token from https://app.pulumi.com/account/tokens
    or hit <ENTER> to log in using your browser:
Just press <ENTER>, and Pulumi will open a browser window asking you to log in using GitHub, GitLab, etc. Once complete, Pulumi CLI will automatically configure access.