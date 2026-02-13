import urllib.parse
import pwd
import pathlib
import tarfile
import shlex
import subprocess
import logging_config


def check_user_exists(username: str) -> bool:
    try:
        pwd.getpwnam(username)  # type: ignore
        logging_config.logger.info(f"[CHECK] User found: '{username}'.")
        return True
    except KeyError as e:
        logging_config.logger.error(
            f"[CHECK] User not found: '{username}'. Details: {e}"
        )
        return False


def check_directory_exists(directory_path: pathlib.Path) -> bool:
    destination = pathlib.Path(directory_path)
    try:
        if destination.is_dir():
            logging_config.logger.info(f"[CHECK] Directory found: '{destination}'.")
            return True
    except OSError as e:
        logging_config.logger.error(
            f"[CHECK] Directory not found: '{destination}'. Details: {e}"
        )
    return False


def check_string_in_file(file_path: pathlib.Path, target_string: str) -> bool:
    try:
        with open(pathlib.Path(file_path), "r") as file:
            for line in file:
                if target_string in line:
                    logging_config.logger.info(
                        f"[CHECK] String '{target_string}' found in '{file_path}'."
                    )
                    return True
    except OSError as e:
        logging_config.logger.error(
            f"[CHECK] Error reading file '{file_path}'. Details: {e}"
        )
        pass
    return False


def extract_archive(
    archive_path: pathlib.Path, destination: pathlib.Path
) -> pathlib.Path:
    try:
        logging_config.logger.info(
            f"[ARCHIVE] Extracting '{archive_path}' to '{destination}'..."
        )
        with tarfile.open(archive_path, "r:gz") as tar_ref:
            tar_ref.extractall(path=destination, filter="tar")
            extracted_folder = pathlib.Path(destination) / tar_ref.getnames()[0]
            logging_config.logger.info(
                f"[ARCHIVE] Extraction complete. Output: '{extracted_folder}'."
            )
            return extracted_folder
    except tarfile.ExtractError as e:
        logging_config.logger.error(
            f"[ARCHIVE] Failed to extract '{archive_path}'. Details: {e}"
        )
        raise


def extract_a_list_of_archive(
    archives: list[pathlib.Path], destination: pathlib.Path
) -> pathlib.Path | None:
    if not archives:
        logging_config.logger.info("[ARCHIVE] No archives to extract — skipping.")
        return None

    try:
        logging_config.logger.info(
            f"[ARCHIVE] Extracting '{archives}' to '{destination}'..."
        )
        for archive in archives:
            with tarfile.open(archive, "r:gz") as tar_ref:
                tar_ref.extractall(path=destination, filter="tar")
                extracted_folder = pathlib.Path(destination)
                logging_config.logger.info(
                    f"[ARCHIVE] Extracted archives: {archives} in '{extracted_folder}'."
                )
                return extracted_folder
        raise ValueError("No archives provided in the list.")
    except tarfile.ExtractError as e:
        logging_config.logger.error(
            f"[ARCHIVE] Failed to extract '{archives}'. Details: {e}"
        )
        raise


def execute_shell_command(
    command: str, manual_check: bool = True
) -> subprocess.CompletedProcess[str]:
    args = shlex.split(command)
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, check=manual_check, timeout=10
        )
        logging_config.logger.info(
            f"[CMD] Command: '{command}' | Return Code: {result.returncode} | Output: {result.stdout.strip()}"
        )
    except subprocess.CalledProcessError as e:
        logging_config.logger.error(
            f"[CMD] Execution failed for '{command}'. Return Code: {e.returncode}. Error: {e.stderr.strip()}"
        )
        raise
    return result


def append_to_bashrc(
    bashrc_path: pathlib.Path, user: str, var_name: str, var_value: pathlib.Path | str
) -> None:
    try:
        with open(bashrc_path, "a") as f:
            f.write(f'\nexport {var_name}="{var_value}"\n')
            logging_config.logger.info(
                f"[ENV] Appended {var_name}='{var_value}' to '{bashrc_path}'."
            )
    except OSError as e:
        logging_config.logger.error(
            f"[ENV] Failed to write to '{bashrc_path}'. Details: {e}"
        )
        pass


def parse_filename_from_url(url: str) -> pathlib.Path:
    try:
        parsed_path = urllib.parse.urlparse(url).path
        filename = pathlib.Path(parsed_path).name
        logging_config.logger.info(f"[PARSE] Extracted filename '{filename}' from URL.")
        return pathlib.Path(filename)
    except ValueError as e:
        logging_config.logger.error(
            f"[PARSE] Failed to parse URL '{url}'. Details: {e}"
        )
        raise
