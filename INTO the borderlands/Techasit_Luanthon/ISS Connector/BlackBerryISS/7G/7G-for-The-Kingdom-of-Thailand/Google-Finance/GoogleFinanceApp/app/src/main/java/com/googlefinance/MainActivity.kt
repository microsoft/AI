package com.googlefinance.app

import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val btnChat = findViewById<Button>(R.id.btn_chat)
        val btnContacts = findViewById<Button>(R.id.btn_contacts)
        val btnGroups = findViewById<Button>(R.id.btn_groups)

        btnChat.setOnClickListener {
            Toast.makeText(this, "Opening Chat...", Toast.LENGTH_SHORT).show()
        }

        btnContacts.setOnClickListener {
            Toast.makeText(this, "Loading Contacts...", Toast.LENGTH_SHORT).show()
        }
        
        btnGroups.setOnClickListener {
             Toast.makeText(this, "Opening Groups...", Toast.LENGTH_SHORT).show()
        }
    }
}
