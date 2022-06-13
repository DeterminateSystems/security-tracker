from collections import defaultdict
from datetime import datetime

from sqlalchemy import func

from tracker import db
from tracker.model import CVE
from tracker.model import CVEGroup
from tracker.model import CVEGroupEntry
from tracker.model import CVEGroupPackage
from tracker.model import Package
from tracker.model.enum import Status
from tracker.model.enum import affected_to_status
from tracker.model.enum import highest_severity
from tracker.model.enum import status_to_affected


def update_group_status():
    updated = []
    groups = (db.session.query(CVEGroup, func.group_concat(CVEGroupPackage.pkgname, ' '))
                .join(CVEGroupPackage)
                .filter(CVEGroup.status.in_([Status.vulnerable, Status.testing]))
                .group_by(CVEGroupPackage.group_id)).all()
    for group, pkgnames in groups:
        pkgnames = pkgnames.split(' ')
        new_status = affected_to_status(status_to_affected(group.status), pkgnames[0], group.fixed)
        if group.status is not new_status:
            updated.append(dict(group=group, old_status=group.status))
        group.status = new_status
    db.session.commit()
    return updated


def recalc_group_status():
    updated = []
    groups = (db.session.query(CVEGroup, func.group_concat(CVEGroupPackage.pkgname, ' '))
                .join(CVEGroupPackage)
                .group_by(CVEGroupPackage.group_id)).all()
    for group, pkgnames in groups:
        pkgnames = pkgnames.split(' ')
        new_status = affected_to_status(status_to_affected(group.status), pkgnames[0], group.fixed)
        if group.status is not new_status:
            updated.append(dict(group=group, old_status=group.status))
        group.status = new_status
    db.session.commit()
    return updated


def recalc_group_severity():
    updated = []
    entries = (db.session.query(CVEGroup, CVEGroupEntry, CVE)
               .join(CVEGroupEntry).join(CVE)
               .group_by(CVEGroupEntry.group_id).group_by(CVE.id)).all()
    issues = defaultdict(set)
    for group, entry, issue in entries:
        issues[group].add(issue)
    for group, issues in issues.items():
        new_severity = highest_severity([issue.severity for issue in issues])
        if group.severity is not new_severity:
            updated.append(dict(group=group, old_severity=group.severity))
        group.severity = new_severity
    db.session.commit()
    return updated
