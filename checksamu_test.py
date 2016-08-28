#!/bin/python
#-*-coding:utf-8:-*-

#バケットのデータ(IPヘッダから)を16進数にしたものを文字として先に取得しておく
dd="45100036092640004006cd84ac010602ac010603041000173102d60e4174fb2a8018821898dc00000101080a000566bc00043c1a0d00"
#チェックサムの足し算計算をする
def checksum_tashi(datas_baye):
	baye_len=len(datas_baye)
	checksum=int(datas_baye[0],16)+int(datas_baye[1],16)
	for counter in xrange(baye_len-2):
        	asd=counter+2
        	checksum+=int(datas_baye[asd],16)
        	xbb=hex(checksum)
		d=len(xbb)
		#桁が大きいならば
		if d==7:
			mae=xbb[0:2]
			ushiro=xbb[3:]
			xd=mae+ushiro
			int_henkan=int(xd,16)
			kakunin=hex(int_henkan+1)
			checksum=int(kakunin,16)
	checksum_keisan=hanten(checksum)
	checksum_ss=hex(checksum_keisan)
	return checksum_ss

#反転する関数
def hanten(checksum):
	nishi=format(checksum,'016b')
	print nishi
	nishi_str=str(nishi)
	lens=len(nishi_str)
	nini=[]
	for d in xrange(lens):
		if nishi_str[d]=='0':
			nini.append('1')
		else:
			nini.append('0')
	nis="".join(nini)

	ju=int(nis,2)
	return ju
	
#データを4つに分ける
def fourspire(batedata):
	checkmoto=[]
	d_len=len(batedata)
	d_lens=d_len/4
	#４つに分けるのと0xをつける
	for s in xrange(d_lens):
		s=s*4
		checkmoto.append('0x'+batedata[s:s+4])
	#チェックサムの部分を0000にする
	#IPならば
	if(d_len<45):
		checkmoto[5]='0x0000'
	else:
	#TCPならば
		checkmoto[8]='0x0000'
	return checkmoto
	
#バイトデータをipとtcpに分ける部分
def ip_tcp(baye):
	ip_bate=baye[:40]
	tcp_bate=baye[40:]
	return ip_bate,tcp_bate

def tcpsect(tcp_data,ip_data):
	#IPデータ長
	packet_len=ip_data[1]
	#データから送信元と送信先を取り出す。
	mae_packet=[]
	for x in xrange(4):
		xs=x-4
		mae_packet.append(ip_data[xs])
	#IPヘッダを取り出す
	ips=ip_data[0]
	ip_head=int(ips[3:4],16)*4
	#パケット長(パケット長-IPヘッダ)
	packettyou=int(packet_len,16)-ip_head
	#プロトコル番号(TCPの場合)
	tcp_protocal='0x0006'
	mae_packet.append(tcp_protocal)
	mae_packet.append(str(hex(packettyou)))
	#リストを連結(疑似ヘッダとTCPのデータをつける)
	for u in xrange(len(tcp_data)):
		mae_packet.append(tcp_data[u])
	return mae_packet

def main():
	#データをIPとTCPに分ける
	ip_bate,tcp_bate=ip_tcp(dd)
	#IPを分割する
	lis=fourspire(ip_bate)
	#IPのチェックサムを計算する
	saikeisan=checksum_tashi(lis)
	#TCPを分割する
	tcplis=fourspire(tcp_bate)
	#TCPのチェックサム計算用意
	TCP_comp=tcpsect(tcplis,lis)
	#TCPチェクサムを計算させる(帰って来た値がtcpのチェックサム)
	tcpcheck=checksum_tashi(TCP_comp)
	print "TCPCHECKSUM"
	print tcpcheck
main()
