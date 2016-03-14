# DHCP Settings for Polycom Phones

We use Polycom phones and do what we can to automate their configuration.  The
first step is setting up the DHCP server.  We use Windows Server and Active 
Directory in the office so we use Microsoft's DHCP server as described below.

1.  Open the DHCP snap-in and browse to the scope where your phone connect.
2.  Right-click on _Policies_ under the _Scope_ and select _New Policy..._.
3.  Give the new policy a name on the _General_ tab.

    ![DHCP-General][DHCP-General]
4.  Specify which clients the policy applies to on the _Conditions_ tab.

    ![DHCP-Conditions][DHCP-Conditions]
5.  Set the options to send on the _Options_ tab.
   
    ![DHCP-Options][DHCP-Options]
6.  Save the new policy then boot the phones to test.

[DHCP-General]: img/DHCP-General.png "DHCP Policy - General"
[DHCP-Conditions]: img/DHCP-Conditions.png "DHCP Policy - Conditions"
[DHCP-Options]: img/DHCP-Options.png "DHCP Policy - Options"

--
Paul Dugas <paul@dugas.cc>
