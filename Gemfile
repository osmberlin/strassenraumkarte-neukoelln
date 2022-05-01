# frozen_string_literal: true
source "https://rubygems.org"

gem "jekyll", "~> 4.2.2"
gem "webrick", "~> 1.7"
# Required to use --livereload option.
# Other gem versions are incompatible with the newer ruby version.
# Via https://talk.jekyllrb.com/t/error-when-running-symbol-not-found-in-flat-namespace-ssl-ctx-set-options/6663/4
gem 'eventmachine', '1.3.0.dev.1', git: 'git@github.com:eventmachine/eventmachine', branch: 'master'

# Themen
gem "minima", "~> 2.5"

# Feature
group :jekyll_plugins do
  gem "kramdown-parser-gfm", "~> 1.1"
  gem "jekyll-redirect-from", "~> 0.16.0" # https://github.com/jekyll/jekyll-redirect-from
  gem "jekyll-feed", "~> 0.12"
end

platforms :mingw, :x64_mingw, :mswin do
  gem "tzinfo", "~> 1.2"
  gem "tzinfo-data"
  gem "wdm", "~> 0.1.1"
end
