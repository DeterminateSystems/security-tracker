from flask import render_template, flash, redirect
from app import app
from app import db
from app.model import CVE, CVEGroup, CVEGroupEntry
from app.model.cve import cve_id_regex
from app.view.error import not_found


@app.route('/issue/<regex("{}"):cve>'.format(cve_id_regex[1:]), methods=['GET'])
@app.route('/<regex("{}"):cve>'.format(cve_id_regex[1:]), methods=['GET'])
def show_cve(cve):
    cve_model = CVE.query.get(cve)
    if not cve_model:
        return not_found()
    groups = (db.session.query(CVEGroupEntry, CVEGroup).filter_by(cve=cve_model).join(CVEGroup)).all()
    groups = sorted(groups, key=lambda item: item[1].created, reverse=True)
    groups = sorted(groups, key=lambda item: item[1].status)

    entry = {
        'cve': cve_model.id,
        'description': cve_model.description,
        'severity': cve_model.severity,
        'remote': cve_model.remote,
        'notes': cve_model.notes,
        'groups': groups,
    }
    return render_template('cve.html',
                           title=cve,
                           entry=entry)
