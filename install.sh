#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_SRC="${SCRIPT_DIR}/plugins"
SKILLS_SRC="${SCRIPT_DIR}/skills"
PLUGINS_DIR="${HOME}/.hermes/plugins"
SKILLS_DIR="${HOME}/.hermes/skills"
HERMES_PIP="${HOME}/.hermes/hermes-agent/venv/bin/pip"

link_dir() {
    local src_dir="$1"
    local target="$2"
    local label="$3"

    if [ -L "${target}" ]; then
        rm "${target}"
    elif [ -e "${target}" ]; then
        echo "Skipping ${label}: ${target} exists and is not a symlink" >&2
        return
    fi

    ln -s "${src_dir}" "${target}"
    echo "Linked ${label} -> ${target}"
}

mkdir -p "${PLUGINS_DIR}"

for plugin_yaml in "${PLUGINS_SRC}"/*/plugin.yaml; do
    [ -e "${plugin_yaml}" ] || continue
    plugin_dir="$(dirname "${plugin_yaml}")"
    plugin_name="$(basename "${plugin_dir}")"

    link_dir "${plugin_dir}" "${PLUGINS_DIR}/${plugin_name}" "plugin ${plugin_name}"

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

mkdir -p "${SKILLS_DIR}"

for category_dir in "${SKILLS_SRC}"/*/; do
    [ -d "${category_dir}" ] || continue
    category_name="$(basename "${category_dir%/}")"
    target_category_dir="${SKILLS_DIR}/${category_name}"

    mkdir -p "${target_category_dir}"

    for entry in "${category_dir}"*; do
        [ -e "${entry}" ] || continue
        entry_name="$(basename "${entry}")"

        link_dir "${entry}" "${target_category_dir}/${entry_name}" "skill ${category_name}/${entry_name}"
    done
done
