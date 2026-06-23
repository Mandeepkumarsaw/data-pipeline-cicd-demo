# Data Pipeline CI/CD Demo..

ETL Lambda (S3 → DynamoDB) with GitHub Actions CI and AWS CodePipeline CD.

## Quick start

1. Read **[SETUP-WALKTHROUGH.md](SETUP-WALKTHROUGH.md)**
2. Set environment variables (`AWS_REGION`, `GITHUB_USER`, etc.)
3. Push code → verify GitHub Actions CI
4. Run `./scripts/setup-aws.sh` → authorize GitHub connection → trigger pipeline

## Repo structure

```
.github/workflows/ci-data-pipeline.yml   # CI: lint + pytest
buildspec.yml                            # CD: CodeBuild steps
lambda/etl_customer/                     # Lambda source
tests/                                   # Unit tests
infra/                                   # IAM + CodePipeline templates (__PLACEHOLDERS__)
scripts/setup-aws.sh                     # One-command AWS provisioning
```

## Architecture

```
git push main → GitHub Actions (CI) + CodePipeline (CD)
CodePipeline: Source → CodeBuild → Lambda Deploy (alias prod)
```


---------------------------------------------------------------------------------------TILL I COVERED-----------------------------------------------------------------------------
# 🚀 AWS CI/CD Pipeline Setup Documentation  
## Project: data-pipeline-cicd-demo

---

# 📌 Overview
This project implements a CI/CD pipeline using AWS services:

- AWS CodePipeline
- AWS CodeBuild
- AWS Lambda
- AWS S3 (Artifact Store)
- AWS CodeStar Connections (GitHub integration)

---

# 🧱 GitHub Repository

https://github.com/Mandeepkumarsaw/data-pipeline-cicd-demo

---

# ☁️ S3 Artifact Bucket

data-pipeline-artifacts-667198667792

---

# 🔗 CodeStar Connection ARN

arn:aws:codeconnections:eu-north-1:667198667792:connection/21d3a5b8-fe98-41e1-9ac7-4a430fcbdfdb

---

# 🔐 IAM Role

data-pipeline-codepipeline-role

---

# 🏗️ CodeBuild Project

etl-customer-build

---

# 📄 buildspec.yml

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.12
    commands:
      - pip install --upgrade pip
      - pip install -r requirements-dev.txt

  pre_build:
    commands:
      - echo "Running tests..."
      - flake8 lambda tests --max-line-length=100 --exclude=__pycache__
      - pytest tests -v

  build:
    commands:
      - echo "Packaging Lambda..."
      - cd lambda/etl_customer
      - zip -r function.zip .

artifacts:
  files:
    - lambda/etl_customer/function.zip
