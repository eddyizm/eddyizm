# eddyizm.com 
Creating a new personal site, blog using django and python. 

# Set up  

This guide assumes you already have python 3 and git installed.  

Clone repository  

    git clone https://github.com/eddyizm/eddyizm.git  

Create a virtual environment  

    python -m venv </path/to/new/virtual/environment>  

Changed directory and activate virtual environment

       cd </path/to/new/virtual/environment>  
       Scripts\activate
       # in bash use this instead
       source Scripts/activate
       cd </pathToGitProject>
Install Django and verify version installed

    pip install django   
    django-admin --version

# podman

build and run 
`podman build -t eddyizm_blog -f ContainerFile`

```  
podman run --name=blog -d -p 8000:8000 -v /home/eddyizm/data:/data:rw -v /home/eddyizm/static:/static:rw -v /home/eddyizm/media:/media:rw --restart unless-stopped localhost/eddyizm_blog
```
       

