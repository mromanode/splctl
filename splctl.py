#!/usr/bin/env python3
import pathlib
import args_config
import web_requests
import os_operations

args = args_config.get_args()


def verify_splunk_user_exists(splunk_user: str) -> bool:
    return os_operations.check_user_exists(splunk_user)


def verify_directory_exists(directory_path: pathlib.Path) -> bool:
    return os_operations.check_directory_exists(directory_path)


def resolve_filename_from_url(splunk_url: str) -> pathlib.Path:
    return os_operations.parse_filename_from_url(splunk_url)


def create_splunk_user(group: str, user: str) -> None:
    os_operations.execute_shell_command(f"groupadd {group}")
    os_operations.execute_shell_command(f"useradd -m -g {group} {user}")


def download_splunk_archive(url: str) -> pathlib.Path:
    return web_requests.download_file(url)


def set_splunk_env_variable(
    user: str, var_name: str, var_value: pathlib.Path | str
) -> None:
    bashrc_path = pathlib.Path(f"/home/{user}/.bashrc")
    target_string = '\nexport {var_name}="{var_value}"\n'
    if not os_operations.check_string_in_file(bashrc_path, target_string):
        os_operations.append_to_bashrc(bashrc_path, user, var_name, var_value)


def extract_splunk_archive(
    archive_path: pathlib.Path, target_path: pathlib.Path
) -> pathlib.Path:
    return os_operations.extract_archive(archive_path, target_path)


def set_directory_ownership(
    group: str, user: str, target_directory: pathlib.Path
) -> None:
    os_operations.execute_shell_command(f"chown -R {user}:{group} {target_directory}")


def enable_splunk_boot_start(group: str, user: str) -> None:
    os_operations.execute_shell_command(
        f"/opt/splunkforwarder/bin/splunk enable boot-start -systemd-managed 1 -user {user} -group {group} --accept-license --answer-yes --no-prompt --gen-and-print-passwd"
    )


def get_latest_download_url() -> str:
    return web_requests.fetch_latest_splunk_url()


def start_splunk_service(splunk_home: pathlib.Path) -> None:
    os_operations.execute_shell_command(f"{splunk_home}/bin/splunk start")


def extract_a_list_of_apps(apps: list[pathlib.Path], destination: pathlib.Path):
    os_operations.extract_a_list_of_archive(apps, destination)


if __name__ == "__main__":
    splunk_user = args.user
    splunk_group = args.group

    splunk_path = args.directory / "splunkforwarder"
    splunk_target_path = args.directory

    splunk_apps = args.apps

    if not verify_splunk_user_exists(splunk_user):
        create_splunk_user(splunk_group, splunk_user)

    if not verify_directory_exists(splunk_path):
        if args.method == "online":
            archive_path = download_splunk_archive(get_latest_download_url())
            extract_splunk_archive(archive_path, args.directory)

        if args.method == "local":
            archive_path = args.archive_path
            extract_splunk_archive(archive_path, args.directory)

        if args.method == "url":
            splunk_url = download_splunk_archive(args.url)
            splunk_archive_filename = resolve_filename_from_url(args.url)
            extract_splunk_archive(splunk_archive_filename, args.install_dir)

    set_splunk_env_variable(splunk_user, "SPLUNK_HOME", splunk_path)
    extract_a_list_of_apps(splunk_apps, splunk_path / "etc/apps/")
    set_directory_ownership(splunk_group, splunk_user, splunk_path)
    enable_splunk_boot_start(splunk_group, splunk_user)
    start_splunk_service(splunk_path)
