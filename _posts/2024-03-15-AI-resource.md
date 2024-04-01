---
title: 'AI resource'
date: 2024-03-15
permalink: /posts/2024/03/AI-resource/
tags:
  - Real Work Practice
---

Mark Some useful AI model、community、dataset、resource here

# Hugging Face

[Official website](https://huggingface.co/): An open source data science and machine learning platform.

* login: jingtaow@buffalo.edu

  ```shell
  # create a repository from the CLI
  # if transformers or datasets is installed  
  $ pip install huggingface_hub 
  
  # Log in using a token from huggingface.co/settings/tokens
  $ huggingface-cli login
  # Create a model or dataset repo from the CLI if needed
  $ huggingface-cli repo create repo_name --type {model, dataset, space}
  
  # clone your model,dataset or space locally
  $ git lfs install 
  $ git clone https://huggingface.co/jingtaoWang/repo_name
  
  # add commit、push any file you want,including large files
  # save files via '.save_pretrained()' or move them there
  $ git add .
  $ git commit -m "commit from $user"
  $ git push 
  
  # In most cases, if your're using one of the compatible libraries,your repo will then be accessible from code. through its identifier: username/repo_name【anyone can load it with】
  tokenizer = AutoTokenizer.from_pretrained("username/repo_name")
  model = AutoModel.from_pretrained("username/repo_name")
  ```

  ## DGA-detector

  [model url](https://huggingface.co/harpomaxx/dga-detector): A DGA lexicographical(字典序) detector using 1DCNN

  * dataset：
    * normal ：alexa-top 1 millions+3161 additional normal domains
    * DGA：resource repository [Andrey Abakumov repository](https://github.com/andrewaeva/DGA)、 [John Bambenek repository](http://osint.bambenekconsulting.com/feeds/)






------

