from flask import render_template, flash, redirect
from app import app
from app import db
from app.model import CVE, CVEGroup, CVEGroupEntry
from app.model.cvegroup import pkgname_regex


@app.route('/package/<regex("{}"):pkgname>'.format(pkgname_regex[1:]), methods=['GET'])
def show_package(pkgname):
    entries = (db.session.query(CVEGroup, CVE).filter_by(pkgname=pkgname).join(CVEGroupEntry).join(CVE)).all()
    groups = set()
    issues = []
    for group, cve in entries:
        groups.add(group)
        issues.append({'cve': cve, 'group': group})

    issues = sorted(issues, key=lambda item: item['cve'].id, reverse=True)
    issues = sorted(issues, key=lambda item: item['group'].status)
    groups = sorted(groups, key=lambda item: item.id, reverse=True)
    groups = sorted(groups, key=lambda item: item.status)

    package = {
        'pkgname': pkgname,
        'groups': {'open': list(filter(lambda group: group.status.open(), groups)),
                   'resolved': list(filter(lambda group: group.status.resolved(), groups))},
        'issues': {'open': list(filter(lambda issue: issue['group'].status.open(), issues)),
                   'resolved': list(filter(lambda issue: issue['group'].status.resolved(), issues))}
    }
    return render_template('package.html',
                           title='Package {}'.format(pkgname),
                           package=package)
