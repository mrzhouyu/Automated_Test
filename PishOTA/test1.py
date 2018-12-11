
import re
s = "http://10.230.1.121/share/ota/SmartRetail-574-20181204-055921/ota/SR-GWSL-M527-A000-FN3-H030-V1.1.251.ota"
lastVersion = re.findall(r"-V(\d{1,3}\.\d{1,3}\.\d{1,3})\.ota", s)[0]

print(lastVersion)