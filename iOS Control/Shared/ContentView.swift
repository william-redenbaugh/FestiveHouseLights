//
//  ContentView.swift
//  Shared
//
//  Created by William Redenbaugh on 12/6/21.
//

import SwiftUI
import Network

struct ContentView: View {
    
    @State var connection: NWConnection?
    var host: NWEndpoint.Host = "127.0.0.1"
    var port: NWEndpoint.Port = 1234
    
    var body: some View {
        VStack(alignment: .center){
            Text("Home Control")
                .multilineTextAlignment(.center)
                .padding()
                .font(.system(size: 30))
            
            
            Button(action:  {
                connect_lights()
                NSLog("Connecting to light server")
            }) {
                Text("Connect To All Devices")
                    .font(.system(size: 20))
                    .padding(9)
                    .background(Color.blue)
                    .foregroundColor(Color.white)
                    .cornerRadius(10)
            }
            
            HStack{
                Button(action:  {
                    // Send a small amount of data over UDP to server
                    let dat = Data()
                    dat.append([255])
                    send(dat)
                }) {
                    Text("Lights On")
                        .font(.system(size: 20))
                        .padding(9)
                        .background(Color.blue)
                        .foregroundColor(Color.white)
                        .cornerRadius(10)
                }
                
                Button(action: /*@START_MENU_TOKEN@*/{}/*@END_MENU_TOKEN@*/) {
                    Text("Lights Off")
                        .font(.system(size: 20))
                        .padding(9)
                        .background(Color.blue)
                        .foregroundColor(Color.white)
                        .cornerRadius(10)
                    
                }
            }
        }
    }
    
    func send(_ payload: Data) {
            connection!.send(content: payload, completion: .contentProcessed({ sendError in
                if let error = sendError {
                    NSLog("Unable to process and send the data: \(error)")
                } else {
                    NSLog("Data has been sent")
                }
            }))
        }
        
        func connect_lights() {
            connection = NWConnection(host: host, port: port, using: .udp)
            connection!.stateUpdateHandler = { (newState) in
                switch (newState) {
                case .preparing:
                    NSLog("Entered state: preparing")
                case .ready:
                    NSLog("Entered state: ready")
                case .setup:
                    NSLog("Entered state: setup")
                case .cancelled:
                    NSLog("Entered state: cancelled")
                case .waiting:
                    NSLog("Entered state: waiting")
                case .failed:
                    NSLog("Entered state: failed")
                default:
                    NSLog("Entered an unknown state")
                }
            }
            
            connection!.viabilityUpdateHandler = { (isViable) in
                if (isViable) {
                    NSLog("Connection is viable")
                } else {
                    NSLog("Connection is not viable")
                }
            }
            
            connection!.betterPathUpdateHandler = { (betterPathAvailable) in
                if (betterPathAvailable) {
                    NSLog("A better path is availble")
                } else {
                    NSLog("No better path is available")
                }
            }
            
            connection!.start(queue: .global())
        }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
