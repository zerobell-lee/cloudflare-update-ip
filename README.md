# Using Cloudflare DNS like DDNS

## Abstract

I'm using Raspberry Pi 3 B+ for my personal web server. However, since I'm using a personal internet line, IP address of my server can be changed in any time. So I decided to use Cloudflare DNS like DDNS, because Cloudflare supports RESTful API to control DNS records. This python script will enable you to update Cloudflare DNS records constantly.

## How it works

This python script is to set on schedule by the scheduler such as crontab. You can adjust how much time it will be excuted. Once it is executed, your server checks a current IP address of itself and compare with the former IP address what is recorded before. If changes on IP address is detected, your server sends some requests to update DNS record. What you have to do is just configure `config.json`

## How to use

### Configuration

Open `config-sample.json` and customize it.

* email : It means Cloudflare account.
* key : Your API Key. You can get this on your Cloudflare Account Profile Page. Check Global API Key.
* zone : It is a API Key to identify DNS. You can check this on Overview of your website.
* ipdir : It is not available anymore. Just ignore it.
* current_ip : Write your current ip. But it is not necessary because when the script is executed for the first time, it will be set automatically.

Save as `config.json` so that the script detects a config file.

If you have to change the name of `config.json` or directories, you can edit `update-ip.py` on yourself. Check out shebang of the python script and adjust it.

### Scheduling

Use scheduler such as crontab. In my case, I edited crontab of root account like this.

<pre>
0 * * * * /home/pi/update_ip.py > update_ip_result
</pre>

It makes your server excute the python script once a hour.