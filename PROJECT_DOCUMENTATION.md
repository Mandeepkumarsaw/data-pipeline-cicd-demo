# AWS Lambda ETL CI/CD Pipeline Documentation

## Project Details

| Property          | Value                                                      |
| ----------------- | ---------------------------------------------------------- |
| Project Name      | AWS Lambda ETL CI/CD Pipeline                              |
| Repository        | https://github.com/Mandeepkumarsaw/data-pipeline-cicd-demo |
| AWS Region        | ap-southeast-2 (Sydney)                                    |
| CodePipeline      | data-pipeline-etl-cd                                       |
| CodeBuild Project | etl-customer-build                                         |
| Lambda Function   | etl-customer-lambda                                        |
| Artifact Bucket   | data-pipeline-artifacts-667198667792                       |

---

# 1. Project Overview

This project implements a complete CI/CD pipeline for deploying an AWS Lambda ETL application using GitHub, AWS CodePipeline, AWS CodeBuild, Amazon S3, and AWS Lambda.

The goal was to automate the deployment of Lambda code whenever changes are pushed to the GitHub repository.

### Objectives

* Store Lambda source code in GitHub
* Automatically trigger deployments on code changes
* Package Lambda source files into a ZIP artifact
* Store artifacts in S3
* Automatically deploy updated code to AWS Lambda
* Remove manual deployment steps

---

# 2. AWS Services Used

* AWS Lambda
* AWS CodePipeline
* AWS CodeBuild
* Amazon S3
* GitHub
* IAM
* CloudWatch Logs
* CodeStar Connection (GitHub Integration)

---

# 3. GitHub Repository Setup

### Repository

```text
https://github.com/Mandeepkumarsaw/data-pipeline-cicd-demo
```

### Branch

```text
main
```

### Repository Structure

```text
data-pipeline-cicd-demo/
│
├── buildspec.yml
│
├── lambda/
│   └── etl_customer/
│       ├── lambda_function.py
│       ├── transform.py
│
└── additional project files
```

### Purpose

The GitHub repository acts as:

* Source of truth
* Version control system
* Pipeline trigger source
* Central code repository

---

# 4. S3 Artifact Bucket

### Bucket Name

```text
data-pipeline-artifacts-667198667792
```

### Purpose

Stores:

* Source artifacts from GitHub
* Build artifacts from CodeBuild
* Deployment packages used by CodePipeline

### Artifact Structure

```text
data-pipeline-etl-cd/
│
├── SourceOutput/
│
└── BuildOutput/
```

---

# 5. GitHub Integration

### Source Provider

```text
GitHub (via GitHub App)
```

### Trigger Configuration

```text
Push Event
Branch: main
```

### Workflow

```text
Git Push
   ↓
GitHub
   ↓
CodePipeline Triggered Automatically
```

No manual pipeline execution is required after a successful push.

---

# 6. IAM Roles

## CodeBuild Service Role

```text
data-pipeline-codebuild-role
```

### Permissions

* S3 Read
* S3 Write
* CloudWatch Logs
* CodeBuild
* CodePipeline

---

## Lambda Execution Role

Required permissions:

* S3 Access
* DynamoDB Access
* CloudWatch Logs

---

# 7. Final Architecture

The final working architecture is:

```text
GitHub Repository
(data-pipeline-cicd-demo)
        │
        ▼
CodePipeline
(data-pipeline-etl-cd)
        │
        ▼
Source Stage
(GitHub via GitHub App)
        │
        ▼
Build Stage
(etl-customer-build)
        │
        ▼
Build Artifact
(function.zip)
        │
        ▼
Deploy Stage
(AWS Lambda Deploy Action)
        │
        ▼
Lambda Function
(etl-customer-lambda)
```

---

# 8. Problems Encountered During Setup

## Issue 1: BuildOutput Artifact Not Found

### Symptoms

Pipeline stages showed:

```text
Source = SUCCESS
Build = SUCCESS
```

But:

```text
BuildOutput folder missing
function.zip not visible
```

### Resolution

Reviewed build logs and artifact configuration.

Confirmed that artifacts section in buildspec.yml was required to export function.zip.

---

## Issue 2: Unable to Locate Deployment ZIP

### Expected

```text
BuildOutput/
└── function.zip
```

### Actual

Only generated artifact objects were visible.

### Resolution

Downloaded the latest BuildOutput artifact from S3 and extracted contents to verify packaging.

---

## Issue 3: buildspec.yml Location Confusion

Initially assumed:

```text
lambda/etl_customer/buildspec.yml
```

### Correct Location

```text
data-pipeline-cicd-demo/
└── buildspec.yml
```

### Resolution

Placed buildspec.yml in repository root.

---

## Issue 4: CodeBuild Reconfiguration

During troubleshooting the original build project was deleted and recreated.

### Final Working Configuration

```text
Project Name: etl-customer-build
Source Provider: No Source
```

### Reason

CodePipeline already supplies source artifacts.

---

## Issue 5: Source Configuration Confusion

While recreating CodeBuild, multiple source options were evaluated:

```text
GitHub
Amazon S3
No Source
```

### Resolution

Selected:

```text
No Source
```

Because CodePipeline provides SourceOutput automatically.

---

## Issue 6: Deploy Strategy Confusion

Initially considered:

```text
CodeBuild Build
      ↓
CodeBuild Deploy
      ↓
aws lambda update-function-code
```

An additional project was created:

```text
etl-customer-deploy
```

### Resolution

Simplified architecture by using:

```text
AWS Lambda Deploy Action
```

inside CodePipeline.

The extra deploy project became unnecessary.

---

# 9. CodeBuild Configuration

## Build Project

```text
etl-customer-build
```

### Source

```text
No Source
```

### Environment

```text
Managed Image
Ubuntu
aws/codebuild/standard:8.0
Container Mode
```

### Service Role

```text
data-pipeline-codebuild-role
```

---

# 10. BuildSpec Configuration

## Final Working buildspec.yml

```yaml
version: 0.2

phases:
  build:
    commands:
      - echo "Packaging Lambda..."
      - cd lambda/etl_customer
      - zip -r ../../function.zip .

artifacts:
  files:
    - function.zip
```

---

## Build Process

### Step 1

```bash
cd lambda/etl_customer
```

Move into Lambda source folder.

### Step 2

```bash
zip -r ../../function.zip .
```

Create deployment package.

### Step 3

```yaml
artifacts:
  files:
    - function.zip
```

Publish artifact to CodePipeline.

---

# 11. CodePipeline Configuration

## Pipeline

```text
data-pipeline-etl-cd
```

---

## Source Stage

### Provider

```text
GitHub (via GitHub App)
```

### Branch

```text
main
```

### Output Artifact

```text
SourceOutput
```

### Status

```text
SUCCESS
```

---

## Build Stage

### Action

```text
BuildAndTest
```

### Provider

```text
AWS CodeBuild
```

### Project

```text
etl-customer-build
```

### Input Artifact

```text
SourceOutput
```

### Output Artifact

```text
BuildOutput
```

### Status

```text
SUCCESS
```

---

## Deploy Stage

### Provider

```text
AWS Lambda
```

### Function

```text
etl-customer-lambda
```

### Input Artifact

```text
BuildOutput
```

### Deployment Package

```text
function.zip
```

### Status

```text
SUCCESS
```

---

# 12. Artifact Verification

Navigate to:

```text
Amazon S3
→ data-pipeline-artifacts-667198667792
→ data-pipeline-etl-cd
→ BuildOutput
```

Download the latest artifact.

Extract the ZIP file.

Verify:

```text
lambda_function.py
transform.py
```

exist inside the deployment package.

---

# 13. Final End-to-End Workflow

```text
Developer
   │
   ▼
Git Push
   │
   ▼
GitHub Repository
   │
   ▼
CodePipeline
   │
   ▼
Source Stage
   │
   ▼
Build Stage
   │
   ├── Read buildspec.yml
   ├── Package Lambda
   ├── Create function.zip
   └── Upload artifact
   │
   ▼
Deploy Stage
   │
   ▼
AWS Lambda Deploy Action
   │
   ▼
etl-customer-lambda
```

---

# 14. Release Change Usage

Use **Release Change** when:

* Testing the pipeline manually
* Re-running the latest commit
* Pipeline configuration changes
* GitHub webhook trigger fails

### Normally Not Required

After:

```bash
git add .
git commit -m "Updated Lambda"
git push origin main
```

CodePipeline starts automatically.

---

# 15. Validation Checklist

### Source Stage

* GitHub commit detected
* Source stage successful

### Build Stage

* Build successful
* Build logs completed
* function.zip generated

### Deploy Stage

* Deploy successful
* Lambda updated automatically

### Lambda Validation

* lambda_function.py present
* transform.py present
* Lambda executes successfully

---

# 16. Lessons Learned

* CodePipeline supplies source artifacts to CodeBuild.
* CodeBuild can use "No Source" when integrated with CodePipeline.
* buildspec.yml should remain in repository root.
* BuildOutput exists only after successful artifact generation.
* AWS Lambda Deploy Action is simpler than maintaining a second deployment CodeBuild project.
* Deploy stage eliminates manual Lambda uploads.
* Build logs are the fastest troubleshooting resource.
* Downloading artifacts from S3 helps verify deployment packages.
* Release Change can manually trigger the latest pipeline execution.

---

# 17. Current Status

```text
GitHub Integration     : SUCCESS
Source Stage           : SUCCESS
Build Stage            : SUCCESS
Artifact Generation    : SUCCESS
Deploy Stage           : SUCCESS
Lambda Deployment      : SUCCESS
CI/CD Workflow         : OPERATIONAL
```

---

# Author

Mandeep Kumar

Project:
AWS Lambda ETL CI/CD Pipeline using GitHub, AWS CodePipeline, AWS CodeBuild, Amazon S3, and AWS Lambda.
