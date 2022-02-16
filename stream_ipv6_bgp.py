#!/usr/bin/env/python3.8

import base64
import json
import urllib2
import ssl
class Server( object ):
   def __init__( self, username, password, address ):
      basicEncode = base64.b64encode( "%s:%s" % ( username, password ) ).strip()
      basicAuthorization = 'Basic %s' %  basicEncode
      self.request_ = urllib2.Request( address )
      self.request_.add_unredirected_header( 'Authorization', basicAuthorization )
      self.request_.get_method = lambda: "POST"

   def runCmds( self, cmds, fmt="json", timeout=None, streaming=False ):
      baseRequest = { "jsonrpc": "2.0", "method": "runCmds",
                      "params": { "version": 1, "cmds": cmds, "format": fmt },
                      "id": "AristaJsonRpcLib", "streaming": streaming }
      try:
         response = urllib2.urlopen( self.request_, data=json.dumps( baseRequest ),
                                     timeout=timeout )
         return json.loads( response.read() )
      except Exception as e:
         print e
         return "timeout"
username = "admin"
password = ""
scheme = "http"
hostname = "hostname_here_please"
ssl._https_verify_certificates( enable=False )
server = Server( username, password, "%s://%s/command-api" % ( scheme, hostname ) )
outputDict = server.runCmds( [ "enable", "show ipv6 bgp" ], "json", streaming=True )
appropriateDict = outputDict['result'][1]
