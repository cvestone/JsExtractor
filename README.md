# JsExtractor
红队渗透中js文件批量信息提取器，提取到的信息方便后续进一步的接口未授权测试等攻击面分析，目前仅是个雏形。最近事情比较多，有空了再优化完善使其内容更丰富，在实战中变得更实用。

最初想法来自于这位师傅的[文章](https://mp.weixin.qq.com/s/weuXxgQR5V9Uz_o15DWG9A)，感谢师傅。
## todo
后续补充。
## 简介

这是一个用于从指定目录下的 JavaScript 文件中提取特定信息的脚本。该脚本可以根据配置文件中定义的正则表达式模式，提取出如 URL、电子邮件地址、电话号码、身份证号、银行卡号、IP 地址、API 密钥等敏感信息。提取的信息可以根据类别进行分类，并可以选择终端输出或保存到文件。

## 特性

- **动态配置**：脚本根据 `regex_patterns.json` 配置文件中的正则表达式模式动态生成菜单项。
- **多类别支持**：支持多个类别，每个类别可以包含多个正则表达式模式。
- **灵活的输出方式**：可以选择在终端输出提取的信息，或者将信息保存到文件。
- **日志记录**：使用日志记录功能，方便调试和跟踪错误。

## 安装

1. **安装 Python**：确保你已经安装了 Python 3.6 或更高版本。
2. **创建虚拟环境**（可选）：
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate  # 在 Windows 上使用 `.\.venv\Scripts\activate`
使用方法
准备配置文件：
将 regex_patterns.json 文件放在脚本的同一目录下。该文件定义了需要匹配的正则表达式及其类别。

运行脚本：

python3 extractor.py <directory_path>
其中 <directory_path> 是你要扫描的目录路径。

选择类别：
脚本启动后，会显示一个菜单，列出所有可用的类别。选择一个类别后，会进一步显示该类别下的所有项目。

选择项目：
选择一个具体的项目或选择“全部”来提取该类别下的所有信息。

选择输出方式：
选择在终端输出提取的信息，或者将信息保存到文件。

配置文件格式
regex_patterns.json 文件是一个 JSON 格式的文件，定义了需要匹配的正则表达式及其类别。示例如下：

{
    "URL": {
        "pattern": "(['\"])(https?://[^\\1]*?)\\1",
        "category": "匹配http和https"
    },
    "Email": {
        "pattern": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,6}",
        "category": "匹配个人敏感信息"
    },
    "Phone": {
        "pattern": "(?<!\\d)(\\+?\\d{1,4}[ \\-]?)?(13\\d{9}|14[579]\\d{8}|15[^4\\D]\\d{8}|166\\d{8}|17[^49\\D]\\d{8}|18\\d{9}|19[189]\\d{8})(?!\\d)",
        "category": "匹配个人敏感信息"
    },
    "IDCard": {
        "pattern": "(^[1-9]\\d{5}(18|19|20)\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\\d{3}[0-9Xx]$)|(^[1-9]\\d{5}\\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])\\d{3}$)",
        "category": "匹配个人敏感信息"
    },
    "BankCard": {
        "pattern": "\\b(?:\\d{4}-){3}\\d{4}|\\d{16,19}\\b",
        "category": "匹配个人敏感信息"
    },
    "IPv4": {
        "pattern": "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b",
        "category": "匹配IP（包括ipv4和ipv6）"
    },
    "IPv6": {
        "pattern": "\\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\\b",
        "category": "匹配IP（包括ipv4和ipv6）"
    },
    "AccessKey": {
        "pattern": "(?i)(access_key|accesskey|access-key).*['\"]([0-9a-zA-Z]{8,40})['\"]",
        "category": "小正则匹配凭据等相关信息"
    },
    "SecretKey": {
        "pattern": "(?i)(secret_key|secretkey|secret-key).*['\"]([0-9a-zA-Z]{16,40})['\"]",
        "category": "小正则匹配凭据等相关信息"
    },
    "APIKey": {
        "pattern": "(?i)(api_key|apikey|api-key).*['\"]([0-9a-zA-Z]{16,40})['\"]",
        "category": "小正则匹配凭据等相关信息"
    },
    "Password": {
        "pattern": "(?i)(password|passwd).*['\"]([^'\"]{8,})['\"]",
        "category": "小正则匹配凭据等相关信息"
    },
    "Token": {
        "pattern": "(?i)(token|access_token|auth_token).*['\"]([0-9a-zA-Z._-]{8,})['\"]",
        "category": "小正则匹配凭据等相关信息"
    },
    "PrivateKey": {
        "pattern": "-----BEGIN (?:RSA )?PRIVATE KEY-----[\\s\\S]*?-----END (?:RSA )?PRIVATE KEY-----",
        "category": "大正则匹配凭据等相关信息"
    },
    "PublicKey": {
        "pattern": "-----BEGIN PUBLIC KEY-----[\\s\\S]*?-----END PUBLIC KEY-----",
        "category": "大正则匹配凭据等相关信息"
    },
    "Certificate": {
        "pattern": "-----BEGIN CERTIFICATE-----[\\s\\S]*?-----END CERTIFICATE-----",
        "category": "大正则匹配凭据等相关信息"
    },
    "AWSAccessKeyID": {
        "pattern": "(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])",
        "category": "常见的云AK匹配"
    },
    "AWSSecretAccessKey": {
        "pattern": "(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])",
        "category": "常见的云AK匹配"
    },
    "GoogleAPIKey": {
        "pattern": "AIza[0-9A-Za-z-_]{35}",
        "category": "常见的云AK匹配"
    },
    "GoogleOAuth": {
        "pattern": "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
        "category": "常见的云AK匹配"
    },
    "SlackToken": {
        "pattern": "xox[baprs]-([0-9a-zA-Z]{10,48})?",
        "category": "常见的key、token匹配"
    },
    "SlackWebhook": {
        "pattern": "https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
        "category": "匹配webhook"
    },
    "FacebookAccessToken": {
        "pattern": "EAACEdEose0cBA[0-9A-Za-z]+",
        "category": "常见的key、token匹配"
    },
    "TwitterAccessToken": {
        "pattern": "[1-9][0-9]+-[0-9a-zA-Z]{40}",
        "category": "常见的key、token匹配"
    },
    "LinkedInClientID": {
        "pattern": "(?i)linkedin(.{0,20})?(?-i)['\"][0-9a-z]{12}['\"]",
        "category": "常见的key、token匹配"
    },
    "LinkedInClientSecret": {
        "pattern": "(?i)linkedin(.{0,20})?['\"][0-9a-z]{16}['\"]",
        "category": "常见的key、token匹配"
    },
    "GitHubAccessToken": {
        "pattern": "(?i)github(.{0,20})?(?-i)['\"][0-9a-zA-Z]{35,40}['\"]",
        "category": "常见的key、token匹配"
    },
    "GitLabAccessToken": {
        "pattern": "(?i)gitlab(.{0,20})?(?-i)['\"][0-9a-zA-Z]{20}['\"]",
        "category": "常见的key、token匹配"
    },
    "Comment": {
        "pattern": "(/\\*[\\s\\S]*?\\*/)|(//.*)",
        "category": "提取多种注释"
    },
    "ChineseText": {
        "pattern": "[\\u4e00-\\u9fff]+",
        "category": "提取潜在有价值的中文信息"
    }
}
脚本功能详解
1. 读取配置文件
脚本通过 load_regex_patterns 函数读取 regex_patterns.json 文件，并将其解析为一个字典。如果文件不存在或格式错误，脚本会记录错误并退出。

2. 提取信息
extract_info 函数会遍历指定目录下的所有 .js 文件，使用配置文件中定义的正则表达式模式提取信息。提取的信息会被存储在一个字典中，键是正则表达式的名称，值是提取到的信息集合。

3. 生成菜单
print_menu 函数会根据配置文件中的类别生成菜单项。用户可以选择一个类别，进一步选择该类别下的具体项目。

4. 处理用户选择
handle_category_choice 函数会根据用户选择的类别生成项目菜单，并返回用户选择的项目列表。

5. 输出结果
print_results 函数会在终端输出提取的信息。
save_results 函数会将提取的信息保存到指定的文件中。
日志记录
脚本使用 logging 模块记录错误和信息，方便调试和跟踪。日志级别设置为 INFO，日志格式为 %(asctime)s - %(levelname)s - %(message)s。

示例
假设你有一个目录 /path/to/js/files，其中包含多个 JavaScript 文件，你可以使用以下命令运行脚本：

python3 extractor.py /path/to/js/files
脚本启动后，会显示一个菜单，列出所有可用的类别。选择一个类别后，会进一步显示该类别下的所有项目。选择一个具体的项目或选择“全部”来提取该类别下的所有信息。最后，选择在终端输出提取的信息，或者将信息保存到文件。

## 示例
![image.png](https://rp01sword.oss-cn-guangzhou.aliyuncs.com/24/20241215183658.png)

