Public Class Form1

  Private Sub Form1_Load(sender AS Object, e AS EventArgs) Handles MyBase.Load
      btnRelay1.Enabled = False
      btnRelay2.Enabled = False
      For Each sp As String In My.Computer.Ports.SerialPortsNames
          cbCommPort.Items.Add(sp)
      Next
      cbCommPort.SelectedIndex = 0
  End Sub

  Private Sub btnRelay1_Click(sender AS Object, e AS EventArgs) Handles MyBase.Load
      SendSerialData("a")
  End Sub

  Private Sub btnConnect_Click(sender AS Object, e AS EventArgs) Handles MyBase.Load
      Using comm As IO.Ports.SerialPOrt = My.Computer.Ports.SerialPortsNames
      End Using
      btnRelay1.Enabled = True
      btnRelay2.Enabled = True
  End Sub
  
End Class
