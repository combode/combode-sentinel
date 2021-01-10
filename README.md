# Combode Sentinel

An all-powerful toolset for Combode.

Sentinel is an autonomous agent for persisting, processing and automating Combode governance objects and tasks.

Sentinel is implemented as a Python application that binds to a local version 1.0.1.1 comboded instance on each Combode 1.0.1.1 Masternode.

This guide covers installing Sentinel onto an existing 1.0.1.1 Masternode in Ubuntu 14.04 / 16.04.

## Installation

### 1. Install Prerequisites

Make sure Python version 2.7.x or above is installed:

    python --version

### 2. Install Sentinel
    
Add string to config file /root/.combodecore/combode.conf

    daemon=1
    server=1
    listen=1
    masternode=1
    masternodeprivkey=PRIVKEY
    externalip=IP
    rpcuser=USER
    rpcpassword=PASSWORD
    rpcport=19192
    rpcallowip=127.0.0.1

Kill comboded and restart
 
    $ ./combode-cli stop
    $ ./comboded

Wait 10 min.

Clone the Sentinel repo and install Python dependencies.

    apt-get update && \
    apt-get -y install python-virtualenv && \
    cd /opt && \
    git clone https://github.com/combode/combode-sentinel combode-sentinel && \
    cd combode-sentinel && \
    virtualenv ./venv && \
    ./venv/bin/pip install -r requirements.txt
    
### 3. Set up Cron

Set up a crontab entry to call Sentinel every minute:

    $ crontab -e

In the crontab editor, add the lines below, replacing '/opt/combode-sentinel' to the path where you cloned combode-sentinel to:

    * * * * * cd /opt/combode-sentinel && ./venv/bin/python bin/sentinel.py >/dev/null 2>&1

### 4. Test the Configuration

Test the config by runnings all tests from the combode-sentinel folder you cloned into

    $ ./venv/bin/py.test ./test

With all tests passing and crontab setup, Sentinel will stay in sync with comboded and the installation is complete

## Configuration

An alternative (non-default) path to the `combode.conf` file can be specified in `sentinel.conf`:

    combode_conf=/path/to/combode.conf

## Troubleshooting

To view debug output, set the `SENTINEL_DEBUG` environment variable to anything non-zero, then run the script manually:

    $ SENTINEL_DEBUG=1 ./venv/bin/python bin/sentinel.py

### License

Released under the MIT license, under the same terms as AzartCore itself. See [LICENSE](LICENSE) for more info.
