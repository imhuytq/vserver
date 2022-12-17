#! /usr/bin/env bash

set -e

# Run worker
celery -A vserver.worker worker -l info -Q main-queue -c 1
