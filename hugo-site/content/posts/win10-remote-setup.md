---
title: "Win10 远程管理 3 条 PowerShell"
date: 2026-07-05
---

**在 Win10 管理员 PowerShell 里逐条执行：**

**1）开远程管理**
```powershell
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.23"; Set-Item WSMan:\localhost\Service\AllowUnencrypted $true; Set-Item WSMan:\localhost\Service\Auth\Basic $true; Restart-Service WinRM
```

**2）连回 Mac 土同学**
```powershell
$cred = Get-Credential; Enter-PSSession -ComputerName 192.168.1.23 -Credential $cred -Authentication Basic
```

执行后会弹出窗口，输 Win10 用户名和密码。

连上后你会看到：
```
[192.168.1.23]: PS C:\Users\你的名字>
```

说明通了，土同学就能直接装 WSL2 + Hermes。
