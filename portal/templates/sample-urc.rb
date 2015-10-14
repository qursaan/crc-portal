defProperty('rate', '.25e6', "Bitrate")
defProperty('modulation','bpsk',"Modulation")
defProperty('freq', '1241M', "Center frequency")
defProperty('runtime', 60, "Run time (s)")


defApplication('benchmark_rx', 'benchmark_rx') { |a|
  a.version(2, 0, 4)
  a.shortDescription = ""
  a.description = ""
  a.path = "echo crc123 | sudo -S ifconfig eth0:0 192.168.10.123;/usr/share/gnuradio/examples/digital/narrowband/benchmark_rx.py"
  a.defProperty('args', "Argument list", '-a',
                {:dynamic => false, :type => :string})
  a.defProperty('freq', "center frequency in Hz", '-f',
                {:dynamic => false, :type => :string})
  a.defProperty('rx-gain', "receive gain in dB", '--rx-gain',
                {:dynamic => false, :type => :string})
  a.defProperty('bitrate', "specify bitrate", '-r',
                {:dynamic => false, :type => :string})
  a.defProperty('modulation', "modulation: psk, cpm, qpsk, dqpsk, gfsk,qam, dbpsk, bpsk, gmsk [default=psk]", '-m',
                {:dynamic => false, :type => :string})
  a.defProperty('constellation-points', "set constellation - power of two for psk, power of 4 for QAM [default=16]", '-p',
                {:dynamic => false, :type => :string})
}

defApplication('benchmark_tx', 'benchmark_tx') { |a|
  a.version(2, 0, 4)
  a.shortDescription = ""
  a.description = ""
  a.path = "echo crc123 | sudo -S ifconfig eth0:0 192.168.10.124;/usr/share/gnuradio/examples/digital/narrowband/benchmark_tx.py"
  a.defProperty('args', "Argument list", '-a',
                {:dynamic => false, :type => :string})
  a.defProperty('freq', "center frequency in Hz", '-f',
                {:dynamic => false, :type => :string})
  a.defProperty('tx-gain', "transmit gain in dB", '--tx-gain',
                {:dynamic => false, :type => :string})
  a.defProperty('tx-amplitude', "transmitter digital amplitude [0,1)  [default=0.25", '--tx-amplitude',
                {:dynamic => false, :type => :string})
  a.defProperty('bitrate', "specify bitrate", '-r',
                {:dynamic => false, :type => :string})
  a.defProperty('modulation', "modulation: psk, cpm, qpsk, dqpsk, gfsk,qam, dbpsk, bpsk, gmsk [default=psk]", '-m',
                {:dynamic => false, :type => :string})
  a.defProperty('constellation-points', "set constellation - power of two for psk, power of 4 for QAM [default=16]", '-p',
                {:dynamic => false, :type => :string})
  a.defProperty('megabytes', "Megabytes to be transmitted", '-M',
                {:dynamic => false, :type => :string})
}




defGroup('rx', 'omf.crc.node3') { |n|
 n.addApplication('benchmark_rx') { |app|
   app.setProperty('args', ' addr=192.168.10.3')
   app.setProperty('freq', property.freq)
   app.setProperty('modulation',property.modulation)
   app.setProperty('bitrate',property.rate)
   app.setProperty('rx-gain','0')
 }

}

defGroup('tx', 'omf.crc.node4') { |n|
 n.addApplication('benchmark_tx') { |app|
   app.setProperty('args', ' addr=192.168.10.2')
   app.setProperty('freq', property.freq)
   app.setProperty('modulation',property.modulation)
   app.setProperty('bitrate',property.rate)
   app.setProperty('tx-gain','0')
   app.setProperty('tx-amplitude','0.5')
   app.setProperty('megabytes','10000')
 }

}

onEvent(:ALL_UP_AND_INSTALLED) { |event|
   # Wait a couple of seconds before proceeding so processes can settle down
  after 10 do



   # Start transmitter application
  info "Start sending packets"
  group("tx").startApplications
  after 20 do
    # Start receiver application
  info "Start receiver app"
  group("rx").startApplications
  end
  end



  # Run for specified runtime
  after property.runtime do

  # Stop benchmark applications
  info "Stop transmitter and receiver"
  allGroups.stopApplications

  after 5 do

  info "done"
  Experiment.done

  end

  end


}
