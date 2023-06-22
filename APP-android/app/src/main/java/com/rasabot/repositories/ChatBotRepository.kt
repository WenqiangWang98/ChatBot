package com.rasabot.repositories

import androidx.lifecycle.LiveData
import com.rasabot.models.BotMessage
import com.rasabot.models.Message
import com.rasabot.models.UserMessage
import com.rasabot.requests.ChatBotApiClient
import com.rasabot.util.Constants

object ChatBotRepository {

    private const val TAG = "ChatBotRepository"

    private val mChatBotApiClient: ChatBotApiClient = ChatBotApiClient

    fun getBotMessages(): LiveData<List<BotMessage>> = mChatBotApiClient.getBotMessages()

    fun getConversation(): LiveData<MutableList<Message>> = mChatBotApiClient.getConversation()

    fun addUserMessageInConversation(userMessage: UserMessage) {
        mChatBotApiClient.addUserMessageInConversation(userMessage)
    }


    fun queryBot(message: String) {
        mChatBotApiClient.queryBot(Constants.USER, message)
    }
}