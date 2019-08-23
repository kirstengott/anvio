#!/usr/bin/env python
# -*- coding: utf-8

import sys
import argparse

import anvio.db as db
import anvio.utils as utils


import anvio.terminal as terminal

from anvio.errors import ConfigError

current_version, next_version = [x[1:] for x in __name__.split('_to_')]




scg_taxonomy_table_name      = 'scg_taxonomy'
scg_taxonomy_structure = ['id'  ,    'gene_caller_id',      'gene_name',  'source' ,  'accession' , 'pourcentage_identity', 't_domain', "t_phylum", "t_class", "t_order", "t_family", "t_genus", "t_species"]
scg_taxonomy_types     = ['numeric', 'numeric' ,             'text'    ,  'text'   ,  'text'   ,       'text'          ,    'text'  ,   'text' ,  'text'  ,  'text'   ,  'text'  ,  'text'  ,   'text'   ]




run = terminal.Run()
progress = terminal.Progress()

def migrate(db_path):
    if db_path is None:
        raise ConfigError("No database path is given.")

    utils.is_contigs_db(db_path)

    contigs_db = db.DB(db_path, None, ignore_version = True)
    if str(contigs_db.get_version()) != current_version:
        raise ConfigError("Version of this contigs database is not %s (hence, this script cannot really do anything)." % current_version)

    progress.new("Actualyse databases ")
    progress.update("...")

    contigs_db.create_table(scg_taxonomy_table_name, scg_taxonomy_structure, scg_taxonomy_types)

    progress.update("Updating version")
    contigs_db.remove_meta_key_value_pair('version')
    contigs_db.set_version(next_version)

    progress.update("Committing changes")
    contigs_db.disconnect()

    progress.end()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple script to upgrade CONTIGS.db from version %s to version %s' % (current_version, next_version))
    parser.add_argument('contigs_db', metavar = 'CONTIGS_DB', help = 'Contigs database at version %s' % current_version)
    args, unknown = parser.parse_known_args()

    try:
        migrate(args.contigs_db)
    except ConfigError as e:
        print(e)
        sys.exit(-1)
