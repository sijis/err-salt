Err plugin for Salt
===

Setup
---
Salt Master must have the salt-api configured and running.
Documentation: http://salt-api.readthedocs.org/en/latest/

Requirements
---
```
pip install salt-pepper
```

Installation
---
```
!repos install https://github.com/sijis/err-salt.git
```

Usage
---
Simple example usage

```
!salt * test.ping
!salt app* cmd.run "ps -ef  | grep python"
```
