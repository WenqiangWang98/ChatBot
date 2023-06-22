package com.rasabot.viewmodels

import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import com.rasabot.models.BotMessage
import com.rasabot.models.Message
import com.rasabot.models.UserMessage
import com.rasabot.repositories.ChatBotRepository
import com.rasabot.util.Constants

class ChatBotViewModel: ViewModel() {

    private val TAG = "ChatBotViewModel"

    private val mChatBotRepository: ChatBotRepository = ChatBotRepository

    fun getBotMessages(): LiveData<List<BotMessage>> = mChatBotRepository.getBotMessages()

    fun getConversation(): LiveData<MutableList<Message>> = mChatBotRepository.getConversation()

    fun addUserMessageInConversation(message: String) {
        mChatBotRepository.addUserMessageInConversation(
            UserMessage(
                message = message,
                id = Constants.USER
            )
        )
    }

    fun queryBot(message: String) {
        mChatBotRepository.queryBot(message)
    }

}