# About

This directory contains simple scripts to gather delay and loss measurements on
AT&T’s backbone network that is published on AT&T’s Web site, and updated every
15 minutes.

You can set up a `cron` job as follows to routinely gather the network data.
```
# Fetch the network latency values of AT&T backbone every 15 minutes.
*/15 * * * * … … … /ext/fetch-latency.sh
# Fetch the network loss values of AT&T backbone every 15 minutes.
*/15 * * * * … … … /ext/fetch-loss.sh
```
