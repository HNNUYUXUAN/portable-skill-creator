# update

UPDATE-1

Read when updating an existing installation. Initially export into a new destination; never overwrite unknown directories. Upgrade uses installed.json hashes to detect user edits and reports conflicts instead of overwriting them. Receiver-only configuration is excluded from releases and preserved during upgrades.

The prior version is kept under the installation grandparent's skill-backups/target-path-hash/previous, outside host skill discovery. Review existing backups rather than deleting automatically. Inspect state after failure. Rollback restores the prior version and retains the current version as rolled-back. Retest affected capabilities; old evidence does not automatically cover changed dependencies. Complete when versions match files, configuration survives, conflicts are explicit and rollback works.
