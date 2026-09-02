# CYPRESS / TRACE Lab - Robot Network Portal

A read only web portal built for the CYPRESS/TRACE lab VPN project at UMBC. It SSHes into the lab's pfSense router, pulls active devices via ARP, and displays them in a clean page that auto refreshes every 30 seconds.

## Files

* `portal.py` - main Flask app (live device table with online/offline status)
* `portal_robots.html` - static HTML preview of the robot portal with UMBC branding
* `requirements.txt` - Python dependencies
* `.env.example` - config template (copy to `.env` and fill in your credentials)

## Setup

You need Python 3.9+ installed.

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Copy the config template and fill in the router password:

   ```
   cp .env.example .env
   ```

3. Connect to the VPN, then run:

   ```
   python3 portal.py
   ```

4. Open your browser and go to `http://127.0.0.1:5000`

## Notes

* Never commit `.env` since it contains the router password
* The portal only works when connected to the CYPRESS VPN
* Robot IPs are pending assignment and will be updated once assigned
