Title
===
Abstract:xxx
## Papar Information
- Title:  `Selenium Login Basic`
- Authors:  `Sinise`
- Preprint: [https://arxiv.org/abs/xx]()
- Full-preprint: [paper position]()
- Video: [video position]()

## Install & Dependence
- allure-pytest==2.13.5
- allure-python-commons==2.13.5
- attrs==25.3.0
- certifi==2025.1.31
- charset-normalizer==3.4.1
- exceptiongroup==1.2.2
- execnet==2.1.1
- Faker==37.0.2
- h11==0.14.0
- idna==3.10
- iniconfig==2.1.0
- Jinja2==3.1.6
- loguru==0.7.3
- MarkupSafe==3.0.2
- numericnormalizer==0.1.0
- numpy==2.0.2
- opencv-python==4.11.0.86
- outcome==1.3.0.post0
- packaging==24.2
- pillow==11.1.0
- pluggy==1.5.0
- py-cpuinfo==9.0.0
- PySocks==1.7.1
- pytesseract==0.3.13
- pytest==8.3.5
- pytest-benchmark==5.1.0
- pytest-html==4.1.1
- pytest-metadata==3.1.1
- pytest-xdist==3.6.1
- python-dotenv==1.0.1
- requests==2.32.3
- selenium==4.29.0
- sniffio==1.3.1
- sortedcontainers==2.4.0
- tomli==2.2.1
- trio==0.29.0
- trio-websocket==0.12.2
- typing_extensions==4.12.2
- tzdata==2025.1
- urllib3==2.3.0
- webdriver-manager==4.0.2
- websocket-client==1.8.0
- wsproto==1.2.0


## Dataset Preparation
| Dataset | Download |
| ---     | ---   |
| dataset-A | [download]() |
| dataset-B | [download]() |
| dataset-C | [download]() |

## Use
- for train
  ```
  pytest tests/test_login.py --alluredir=allure-results
  ```
- for test
  ```
  rm -rf allure-results && pytest -n 2 --alluredir=allure-results
  ```
## Pretrained model
| Model | Download |
| ---     | ---   |
| Model-1 | [download]() |
| Model-2 | [download]() |
| Model-3 | [download]() |


## Directory Hierarchy
```
|—— .DS_Store
|—— .gitignore
|—— allure-results
|—— assets
|    |—— style.css
|—— captcha.png
|—— logs
|    |—— test_results.json
|—— pages
|    |—— __init__.py
|    |—— __pycache__
|        |—— __init__.cpython-39.pyc
|        |—— login_page.cpython-39.pyc
|    |—— checkout_page.py
|    |—— login_page.py
|—— processed_captcha.png
|—— report.html
|—— requirements.txt
|—— screenshots
|—— test_api.py
|—— test_login.py
|—— test_results.json
|—— test_results.log
|—— tests
|    |—— __init__.py
|    |—— __pycache__
|        |—— __init__.cpython-39.pyc
|        |—— test_login.cpython-39-pytest-8.3.5.pyc
|    |—— test_api.py
|    |—— test_login.py
|—— testx_login0.py
|—— testx_login1.py
|—— testx_login2.py
|—— wa.py
```
## Code Details
### Tested Platform
- software
  ```
  OS: Debian unstable (May 2021), Ubuntu LTS
  Python: 3.8.5 (anaconda)
  PyTorch: 1.7.1, 1.8.1
  ```
- hardware
  ```
  CPU: Apple M2 Air
  ```
### Hyper parameters
```
```
## References
- [paper-1]()
- [paper-2]()
- [code-1](https://github.com)
- [code-2](https://github.com)
  
## License

## Citing
If you use xxx,please use the following BibTeX entry.
```
```
