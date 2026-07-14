# 中国境内服务的安卓app-mihomo规则集

## 手工维护格式
list目录存储格式
文件命名格式 list/中文公司名@英文公司编码.yaml
举例
list/腾讯@tencent.yaml

```yaml
app-list:
  - "com.tencent.mm": 微信
```

## 运行脚本生成
`python3 generate_rules.py`

会生成clash_android_rules.yaml

## mihomo规则集用法

```yaml
rule-providers:
  china_android_app:
    behavior: classical
    interval: 86400
    path: ./ruleset/china_android_app.yaml
    type: http
    url: https://raw.githubusercontent.com/whp98/CHINA-MAINLAND-ANDROID-APP/refs/heads/main/clash_android_rules.yaml

#可选配置(使用代理组手工切换直连还是代理)
rules:
 - RULE-SET,china_android_app,中国安卓app
proxy-groups:
  - name: 中国安卓app
    disable-udp: false
    lazy: true
    proxies:
    - DIRECT
    - 代理总出口
    timeout: 5000
    type: select
    url: https://www.google.com/generate_204
```
