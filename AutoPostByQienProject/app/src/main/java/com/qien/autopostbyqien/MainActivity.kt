package com.qien.autopostbyqien

import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import okhttp3.*
import java.io.IOException

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient()
    private lateinit var scope: CoroutineScope

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        scope = CoroutineScope(Dispatchers.IO)

        val tokenInput = findViewById<EditText>(R.id.tokenInput)
        val webhookInput = findViewById<EditText>(R.id.webhookInput)
        val channelIdInput = findViewById<EditText>(R.id.channelInput)
        val messageInput = findViewById<EditText>(R.id.messageInput)
        val delayInput = findViewById<EditText>(R.id.delayInput)
        val totalInput = findViewById<EditText>(R.id.totalInput)
        val kirimButton = findViewById<Button>(R.id.kirimButton)

        kirimButton.setOnClickListener {
            val token = tokenInput.text.toString().trim()
            val webhook = webhookInput.text.toString().trim()
            val channelId = channelIdInput.text.toString().trim()
            val message = messageInput.text.toString()
            val delay = delayInput.text.toString().toIntOrNull() ?: 0
            val total = totalInput.text.toString().toIntOrNull() ?: 1

            scope.launch {
                for (i in 1..total) {
                    val result = sendMessage(token, channelId, message)
                    sendWebhook(webhook, "📢 Loop $i: $result")

                    if (i != total) delay(delay * 1000L)
                }
            }
        }
    }

    private fun sendMessage(token: String, channelId: String, content: String): String {
        val json = "{"content": "$content"}"
        val body = RequestBody.create(MediaType.parse("application/json"), json)
        val request = Request.Builder()
            .url("https://discord.com/api/v10/channels/$channelId/messages")
            .addHeader("Authorization", token)
            .post(body)
            .build()

        return try {
            val response = client.newCall(request).execute()
            "[${response.code()}] ${response.message()}"
        } catch (e: IOException) {
            "❌ Error: ${e.message}"
        }
    }

    private fun sendWebhook(webhook: String, message: String) {
        val json = "{"content": "$message"}"
        val body = RequestBody.create(MediaType.parse("application/json"), json)
        val request = Request.Builder()
            .url(webhook)
            .post(body)
            .build()

        try {
            client.newCall(request).execute()
        } catch (_: IOException) {
        }
    }
}