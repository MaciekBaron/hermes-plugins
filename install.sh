#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="${HOME}/.hermes/plugins"
HERMES_PIP="${HOME}/.hermes/hermes-agent/venv/bin/pip"

mkdir -p "${PLUGINS_DIR}"

for plugin_yaml in "${SCRIPT_DIR}"/*/plugin.yaml; do
    [ -e "${plugin_yaml}" ] || continue
    plugin_dir="$(dirname "${plugin_yaml}")"
    plugin_name="$(basename "${plugin_dir}")"
    target="${PLUGINS_DIR}/${plugin_name}"

    if [ -L "${target}" ]; then
        rm "${target}"
    elif [ -e "${target}" ]; then
        echo "Skipping ${plugin_name}: ${target} exists and is not a symlink" >&2
        continue
    fi

    ln -s "${plugin_dir}" "${target}"
    echo "Linked ${plugin_name} -> ${target}"

    requirements_txt="${plugin_dir}/requirements.txt"
    if [ -e "${requirements_txt}" ]; then
        if [ -x "${HERMES_PIP}" ]; then
            echo "Installing requirements for ${plugin_name}"
            "${HERMES_PIP}" install -r "${requirements_txt}"
        else
            echo "Skipping requirements for ${plugin_name}: ${HERMES_PIP} not found" >&2
        fi
    fi
done
