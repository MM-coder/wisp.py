import requests
import classes

def url_join(*args):
    """Combine URL parts to get the full endpoint address."""
    return '/'.join(arg.strip('/') for arg in args)


class Wispy(object):

    def __init__(self, url, api_key):
        self.api_key = api_key
        self.url = url

    
    def get_headers(self):
        '''
            Returns headers to be used universally throughout all requests
        '''
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/vnd.wisp.v1+json',
            'Content-Type': 'application/json',
        }

        return headers


    def make_get_request(self, endpoint: str, json: bool):
        requestUrl = url_join(self.url, endpoint)
        headers = self.get_headers()
        r = requests.get(url=requestUrl, headers=headers)
        r.raise_for_status()
        if json:
            return r.json()
        else:
            return r


    def make_post_request(self, endpoint: str, data, json: bool):
        requestUrl = url_join(self.url, endpoint)
        headers = self.get_headers()
        r = requests.post(url=requestUrl, headers=headers, data=data)
        r.raise_for_status()
        if json:
            return r.json()
        else:
            return r


    def get_all_servers(self):
        r = self.make_get_request(endpoint="api/client", json=True)
        l = []
        for i in range(r['meta']['pagination']['total']):
            if i + 1 != 1:
                # Iterate through pages
                r = self.make_get_request(endpoint=f"api/client/{i+1}", json=True)
                for server in r['data']:
                    if server['object'] == "server":
                        attributes = server['attributes']
                        l.append(classes.Server(server_owner=bool(attributes['server_owner']), identifier=attributes['identifier'], name=attributes['name'], description=attributes['description'], limits=attributes['limits'], databases=attributes['feature_limits']['databases']))
                    else:
                        pass
            else:
                # Utilize base endpoint
                r = self.make_get_request(endpoint=f"api/client", json=True)
                for server in r['data']:
                    if server['object'] == "server":
                        attributes = server['attributes']
                        l.append(classes.Server(server_owner=bool(attributes['server_owner']), identifier=attributes['identifier'], name=attributes['name'], description=attributes['description'], limits=attributes['limits'], databases=attributes['feature_limits']['databases']))
                    else:
                        pass
        return l

    def get_server(self, identifier: str):
        r = self.make_get_request(endpoint=f"api/client/servers/{identifier}", json=True)
        if r['object'] == 'server':
            attributes = r['attributes']
            return classes.Server(server_owner=bool(attributes['server_owner']), identifier=attributes['identifier'], name=attributes['name'], description=attributes['description'], limits=attributes['limits'], databases=attributes['feature_limits']['databases'])
        else:
            pass

    def get_server_utilization(self, identifier: str):
        r = self.make_get_request(endpoint=f"api/client/servers/{identifier}/utilization", json=True)
        if r['object'] == 'stats':
            attributes = r['attributes']
            return classes.Stats(state=attributes['state'], memory=attributes['memory'], cpu=attributes['cpu'], disk=attributes['disk'], players=attributes['players'], query=None)
        else:
            pass

    def start_server(self, identifier: str):
        r = self.make_post_request(endpoint=f"api/client/servers/{identifier}/power", data={'signal': 'start'}, json=True)
        return r

    def stop_server(self, identifier: str):
        r = self.make_post_request(endpoint=f"api/client/servers/{identifier}/power", data={'signal': 'stop'}, json=True)
        return r

    def kill_server(self, identifier: str):
        r = self.make_post_request(endpoint=f"api/client/servers/{identifier}/power", data={'kill': 'stop'}, json=True)
        return r

    def restart_server(self, identifier: str):
        r = self.make_post_request(endpoint=f"api/client/servers/{identifier}/power", data={'kill': 'restart'}, json=True)
        return r

    def send_command(self, identifier: str, command: str):
        r = self.make_post_request(endpoint=f"api/client/servers/{identifier}/command", data={'command': command}, json=True)
        return r