#!/bin/bash

# Start the first process
python ./odoo_operator/cli.py  &

# Start the second process
python run_server.py  &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?