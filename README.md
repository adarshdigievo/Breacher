# Breacher
A script to find admin login pages and EAR vulnerabilites. Supports multiple domain scanning (specify domain list in a file)

#### Features
- [x] Multi-threading on demand
- [x] Big path list (482 paths)
- [x] Supports php, asp and html extensions
- [x] Checks for potential EAR vulnerabilites
- [x] Checks for robots.txt
- [x] Support for custom patns

### Usages
- specify list of domains to scan in a file domainlist.txt. The output will be saved to output.txt.

- Check all paths with php extension
```
python breacher--type php
```
- Check all paths with php extension with threads
```
python breacher --type php --fast
```
- Check all paths without threads
```
python breacher 
```
- Adding a custom path. For example if you want all paths to start with /data (example.com/data/...) you can do this:
```
python breacher  --path /data
```
<b>Note: </b> When you specify an extension using <b>--type</b> option, Breacher includes paths of that extension as well as paths with no extensions like <b>/admin/login</b>
