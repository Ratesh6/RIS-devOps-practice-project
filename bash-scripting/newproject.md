#  Automated File Backup Tool

This project is a fully automated, command-line-based file backup tool written in Bash. It allows users to back up one or multiple files by simply providing the file paths when running the script. The script dynamically creates backup directories, applies timestamped or custom .bak naming, compresses backups if requested, and can even upload backups to a remote server. It also includes features for backing up recently modified files, keeping a log of all backup operations, and safely managing old backups.

The goal is to create a portable, intelligent, and flexible backup solution that adapts to a variety of real-world use cases, all from the terminal.

##  What This Project Does

### 🔹 1. Accepts File(s) as Input
You can back up one or many files at once:

```bash
./backup.sh file1.txt file2.jpg /home/user/docs/report.pdf
```

### 🔹 2. Auto-Creates Backup Folder
The script automatically creates a folder for the backup, named using the current timestamp:

```bash
~/backups/2025-08-06_15-22-00/
```

### 🔹 3. Applies Smart File Naming
Each file is backed up either:

- Inside a timestamped folder as-is, or
- With a .bak extension or timestamp in the filename:

```
report.docx → report.docx.bak
```

This helps identify the backup file even when stored individually.

### 🔹 4. Supports Compression with Flags
You can use a flag like `--compress` to compress all the files into a .tar.gz archive:

```bash
./backup.sh --compress file1.txt file2.jpg
```

The compressed file will be named with a timestamp.

### 🔹 5. Keeps a Log of All Actions
Every time the script runs, it logs:

- What files were backed up
- Where they were saved
- Time of backup
- Success or failure messages

This is saved in a log file (e.g., `backup.log`) for transparency and debugging.

### 🔹 6. Performs Remote Backup (Optional)
Using a `--remote` flag or config setting, the script can upload backups to a remote server via scp or rsync:

```bash
./backup.sh --remote file1.txt
```

The remote destination and login credentials are defined in the script or a config file.

### 🔹 7. Deletes Older Backups (Rotation)
You can specify how many backups to keep (e.g., the last 5). Older ones are automatically deleted to save space.

### 🔹 8. Auto-Backs Up Recently Modified Files
With a flag like `--recent`, the script can scan directories for files modified within the last day (or any set time window) and back them up:

```bash
./backup.sh --recent 1d
```

This allows for scheduled backups of only new/changed content.

### 🔹 9. Optional Log Toggle
You can disable logging for cleaner runs using `--no-log`, if desired.

### 🔹 10. Help Menu
Running the script with `--help` shows a usage guide:

```bash
./backup.sh --help
```

## Skills You'll Use and Learn

- Bash scripting (variables, loops, conditionals)
- File system navigation and file I/O
- Timestamps with the date command
- Compression with tar and gzip
- Uploads with scp or rsync
- Using command-line flags (getopts or manual parsing)
- Logging and error handling
- Automating tasks and cleanup logic

##  Why This Project Is Valuable

- **It's practical** — you can use it every day
- **It's flexible** — works with any file, any user, any system
- **It's a launchpad** — you can adapt it for backups, deployments, logging systems, and more
- **It teaches real automation skills**, similar to those used in DevOps, IT, and sysadmin jobs

##  Safety Design

- The original files are never modified or deleted
- Backups are stored in dedicated, user-defined directories
- All file checks are performed before any operation
- Logs allow you to trace and debug anything that goes wrong

## ✅ Example Usages

**Backup a file:**
```bash
./backup.sh ~/Documents/resume.pdf
```

**Backup multiple files with compression:**
```bash
./backup.sh --compress file1.txt file2.txt
```

**Backup recently modified files:**
```bash
./backup.sh --recent 2d
```

**Send to remote server:**
```bash
./backup.sh --remote ~/Downloads/notes.md
```

This is more than just a script — it's your personal, command-line-powered backup system.

