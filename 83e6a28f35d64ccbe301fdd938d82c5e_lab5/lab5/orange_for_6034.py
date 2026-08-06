# -*- coding: utf-8 -*-
import sys
import os

# 외부 데이터 리더 모듈 임포트
from data_reader import *


def bill_identifier(bill_data):
    text = bill_data['number']
    if not text:
        text = bill_data['name'].replace(r'\W', '_')
    return str(bill_data['id']) + ":" + text


def write_congress_data(legislators, filename,
                        descriptions=None, unknown_column=-1):
    f = open(filename, "w")
    num_votes = len(legislators[0]['votes'])

    if descriptions:
        if len(descriptions) != len(legislators[0]['votes']):
            print "%s: %d != %d" % (filename, len(descriptions), len(legislators[0]['votes']))
            print descriptions[0]
        print >> f, "party\t" + "\t".join([bill_identifier(v) for v in descriptions])
    else:
        print >> f, "party\t" + "\t".join(map(str, range(num_votes)))

    print >> f, "\t".join(["discrete" for i in xrange(num_votes + 1)])
    print >> f, "\t".join(["" for i in xrange(-1, unknown_column)]),
    print >> f, "class\t",
    print >> f, "\t".join(["" for i in xrange(unknown_column + 1, num_votes)])

    for legislator in legislators:
        print >> f, legislator['party'] + "\t" + "\t".join(map(str, legislator['votes']))

    f.close()


if __name__ == "__main__":
    print "국회 투표 데이터 변환을 시작합니다..."

    for term in ["H004", "S109", "H109", "S110", "H110"]:
        try:
            write_congress_data(read_congress_data(term + ".ord"), term + ".tab",
                                descriptions=read_vote_data(term + "desc.csv"),
                                unknown_column=-1)
            print "성공적으로 변환됨: " + term + ".tab"
        except Exception as e:
            print "오류 발생 (", term, "): ", e

    print "모든 작업이 완료되었습니다."