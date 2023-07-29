
import argparse
import git
import json
import sqlite3
from contextlib import closing
from typing import List


def connect_to_db(db_name: str) -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def create_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            hash TEXT,
            author TEXT,
            date TEXT,
            content TEXT
        )
    ''')


def get_repo(repo_path: str) -> git.Repo:
    return git.Repo(repo_path)


def get_commits(repo: git.Repo, filepath: str) -> List[git.Commit]:
    return list(repo.iter_commits(paths=filepath))


def get_commit_content(commit: git.Commit, filepath: str) -> str:
    try:
        return json.dumps(
            json.loads(commit.tree[filepath].data_stream.read().decode()),
            indent=4)
    except KeyError:
        return ''


def insert_commit(cursor: sqlite3.Cursor, commit: git.Commit, content: str) -> None:
    cursor.execute('''
        INSERT INTO commits (hash, author, date, content)
        VALUES (?, ?, ?, ?)
    ''', (commit.hexsha, str(commit.author), str(commit.authored_datetime),
          content))


def process_commits(repo_path: str, filepath: str, db_name: str) -> None:
    conn = connect_to_db(db_name)
    with closing(conn):
        cursor = conn.cursor()
        with closing(cursor):
            create_table(cursor)
            repo = get_repo(repo_path)
            commits = get_commits(repo, filepath)
            for commit in commits:
                content = get_commit_content(commit, filepath)
                insert_commit(cursor, commit, content)
            conn.commit()


def main():
    parser = argparse.ArgumentParser(
        description='Process commits of a specific file in a git repo.')
    parser.add_argument('repo_path', type=str, help='Path to the git repository')
    parser.add_argument('filepath', type=str, help='Path to the file within the git repository')
    parser.add_argument('db_name', type=str, help='Name of the SQLite database')

    args = parser.parse_args()

    process_commits(args.repo_path, args.filepath, args.db_name)


if __name__ == "__main__":
    main()
